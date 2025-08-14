import numpy as np
import tkinter as tk
import tensorflow as tf
from tkinter import Canvas, Label, Button
from PIL import Image, ImageDraw, ImageOps

MODEL_PATH = "mnist_cnn.h5"


class DrawApp:
    def __init__(self, master):
        self.master = master
        master.title("MNIST Digit Recognizer")
        master.configure(bg="#222")

        self.canvas_size = 560
        self.brush_radius = 16
        self.canvas = Canvas(
            master,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="white",
            highlightthickness=2,
            highlightbackground="#444",
        )
        self.canvas.grid(row=0, column=0, rowspan=6, padx=20, pady=20)

        self.label = Label(
            master,
            text="Draw a digit!",
            font=("Segoe UI", 20, "bold"),
            fg="#fff",
            bg="#222",
        )
        self.label.grid(row=0, column=1, sticky="w", padx=10, pady=(30, 0))

        self.heatmap_frame = tk.Frame(master, bg="#222")
        self.heatmap_frame.grid(row=1, column=1, sticky="nw", padx=10)

        self.clear_btn = Button(
            master,
            text="Clear",
            command=self.clear,
            font=("Segoe UI", 12),
            bg="#444",
            fg="#fff",
            activebackground="#666",
            activeforeground="#fff",
        )
        self.clear_btn.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_paint)
        self.last_x = None
        self.last_y = None
        self.image = Image.new("L", (self.canvas_size, self.canvas_size), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.model = tf.keras.models.load_model(MODEL_PATH)

        self.heatmap_bars = []
        self.heatmap_labels = []
        for i in range(10):
            bar = Canvas(
                self.heatmap_frame,
                width=200,
                height=24,
                bg="#333",
                highlightthickness=0,
            )
            bar.grid(row=i, column=1, padx=5, pady=2)
            label = Label(
                self.heatmap_frame,
                text=str(i),
                font=("Segoe UI", 14),
                fg="#fff",
                bg="#222",
                width=2,
            )
            label.grid(row=i, column=0, padx=5)
            self.heatmap_bars.append(bar)
            self.heatmap_labels.append(label)

    def start_paint(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def paint(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                event.x,
                event.y,
                width=self.brush_radius * 2,
                fill="black",
                capstyle=tk.ROUND,
                smooth=True,
            )
            self.draw.line(
                [self.last_x, self.last_y, event.x, event.y],
                fill="black",
                width=self.brush_radius * 2,
            )
        else:
            x1, y1 = (event.x - self.brush_radius), (event.y - self.brush_radius)
            x2, y2 = (event.x + self.brush_radius), (event.y + self.brush_radius)
            self.canvas.create_oval(x1, y1, x2, y2, fill="black", outline="black")
            self.draw.ellipse([x1, y1, x2, y2], fill="black")
        self.last_x = event.x
        self.last_y = event.y
        self.predict()

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (self.canvas_size, self.canvas_size), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.label.config(text="Draw a digit!")
        for bar in self.heatmap_bars:
            bar.delete("all")
        self.last_x = None
        self.last_y = None

    def predict(self):
        img = self.image.resize((28, 28))
        img = ImageOps.invert(img)
        arr = np.array(img).astype("float32") / 255.0
        arr = np.expand_dims(arr, axis=(0, -1))
        preds = self.model.predict(arr)[0]
        pred_digit = int(np.argmax(preds))
        self.label.config(text=f"Predicted: {pred_digit}")
        self.update_heatmap(preds)

    def update_heatmap(self, preds):
        max_prob = np.max(preds)
        for i, bar in enumerate(self.heatmap_bars):
            bar.delete("all")
            prob = preds[i]
            r = int(255 * prob)
            g = int(64 * (1 - prob))
            b = int(255 * (1 - prob))
            color = f"#{r:02x}{g:02x}{b:02x}"
            bar.create_rectangle(0, 0, int(prob * 200), 24, fill=color, outline="")
            bar.create_text(
                180, 12, text=f"{prob:.2%}", fill="#fff", font=("Segoe UI", 12, "bold")
            )


def main():
    root = tk.Tk()
    app = DrawApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

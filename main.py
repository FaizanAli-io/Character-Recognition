import numpy as np
import pygame
import sys
import cv2
from matplotlib import pyplot
from tensorflow.keras.models import load_model

pygame.init()

scW, scH = 900, 552
screen = pygame.display.set_mode((scW, scH))
pygame.display.set_caption("Scribble")
pygame.mouse.set_cursor(*pygame.cursors.diamond)
clock = pygame.time.Clock()
black, white = (0, 0, 0), (255, 255, 255)
green, red, blue = (0, 255, 0), (255, 0, 0), (0, 0, 255)


def close():
    pygame.quit()
    sys.exit()


class Doodle:
    def __init__(self, model):
        self.model = model
        self.boxsize = 8
        self.dims = 64
        self.offset = 20
        self.doodle_box = pygame.Rect(
            self.offset, self.offset, self.dims*self.boxsize, self.dims*self.boxsize)
        self.enter_box = pygame.Rect(680, 20, 200, 50)
        self.delete_box = pygame.Rect(680, 90, 200, 50)
        self.matrix = np.zeros((self.dims, self.dims))
        self.matrix.fill(255)
        self.grid = [[pygame.Rect(i*self.boxsize+self.offset, j*self.boxsize+self.offset,
                                  self.boxsize, self.boxsize) for i in range(self.dims)] for j in range(self.dims)]
        self.char_str = ""

    def render(self):
        for i in range(self.dims):
            for j in range(self.dims):
                color = white if self.matrix[i, j] else black
                pygame.draw.rect(screen, color, self.grid[i][j])
        pygame.draw.rect(screen, green, self.enter_box)
        pygame.draw.rect(screen, red, self.delete_box)

    def enter(self):
        ref = [str(i) for i in range(10)] + [chr(i) for i in range(65, 91)]
        image = cv2.resize(self.matrix, (128, 128))
        image = image.reshape((1, 128, 128, 1))
        result = ref[np.argmax(self.model.predict(image))]
        print(result)
        self.matrix.fill(255)

    def delete(self):
        self.char_str = self.char_str[:-1]

    def clicked(self, x, y):
        x, y = (x-self.offset)//self.boxsize, (y-self.offset)//self.boxsize
        self.matrix[y-1:y+2, x-1:x+2] = 0


model = load_model("models\mymodel")
mydoodle = Doodle(model)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                close()
            elif event.key == pygame.K_RETURN:
                mydoodle.enter()
            elif event.key == pygame.K_BACKSPACE:
                mydoodle.delete()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mydoodle.enter_box.collidepoint(pygame.mouse.get_pos()):
                mydoodle.enter()
            elif mydoodle.delete_box.collidepoint(pygame.mouse.get_pos()):
                mydoodle.delete()

    if pygame.mouse.get_pressed(3)[0]:
        pos = pygame.mouse.get_pos()
        if mydoodle.doodle_box.collidepoint(pos):
            mydoodle.clicked(pos[0], pos[1])

    screen.fill(black)
    mydoodle.render()
    pygame.display.flip()
    clock.tick(100)

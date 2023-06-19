import os, random
from shutil import copy2

def listfoldersize():
    for name in os.listdir("./train"):
        print(name, ':', len(os.listdir(f"./train/{name}")))

def copy_data(quant):
    for letter in os.listdir("./by_class"):
        folders = [direc for direc in os.listdir(f"./by_class/{letter}")
            if os.path.isdir(f"./by_class/{letter}/{direc}")]
        
        newperfol = quant // len(folders)
        if letter.isnumeric():
            newperfol *= 2
        count = 0
        
        for fold in folders:
            try:
                pictures = random.choices(os.listdir(f"./by_class/{letter}/{fold}"), k = newperfol)
            except:
                continue

            for pic in pictures:
                readpath = f"./by_class/{letter}/{fold}/{pic}"
                writepath = f"./train/{letter[0]}/{letter}_{count}.png"
                
                try:
                    copy2(readpath, writepath)
                    count += 1
                except:
                    pass

        print(f"Moved {count} files from ./by_class/{letter}  >>  ./train/{letter[0]}")
    
    listfoldersize()

def equalize(level):
    for folder in os.listdir("./picture_database"):
        extra = len(os.listdir("./picture_database/" + folder)) - level
        deadbox = random.choices(os.listdir("./picture_database" + folder), k = extra)
        
        for pic in deadbox:
            try:
                os.remove(f"./picture_database/{folder}/{pic}")
            except:
                pass
        
        print("Cleaned Folder", folder)
    
    listfoldersize()

def rename():
    for folder in os.listdir("./train"):
        for i, image in enumerate(os.listdir("./train/" + folder)):
            os.rename(f"./train/{folder}/{image}", f"./train/{folder}/sample{i}.png")
        print("Renamed Folder", folder)

def validation_split(quant):
    errors, success = 0, 0
    for folder in os.listdir("./train"):
        #quant = len(os.listdir("./train/" + folder)) % 1000
        pictures = random.choices(os.listdir("./train/" + folder), k = quant)

        for pic in pictures:
            readpath = f"./train/{folder}/{pic}"
            writepath = f"./test/{folder}/{pic}"
            
            try:
                os.replace(readpath, writepath)
                success += 1
            except:
                errors += 1
    
    print(f"Moved {success} Files with {errors} Exceptions")
    listfoldersize()

# for image in os.listdir("./data"):
#     num = int(image[3:6])
#     folders = os.listdir("./dataset")
#     readpath = f"./data/{image}"
#     writepath = f"./dataset/{folders[num-1]}"
#     try:
#         copy2(readpath, writepath)
#     except:
#         print("Error")

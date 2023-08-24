import os

from PIL import Image


def gen_img():
    monitors = None
    try:
        a = 1
        # monitors = get_monitors()
    except:
        print('Error getting monitors')
        return None
    width, height = 1920, 1080
    new_image = Image.new("RGB", (width, height), (0, 0, 0))

    wallpaper = Image.open(os.getcwd() + '/src/powerfullbackground/ressources/fantasy-2750995_1920.jpeg')
    wallpaper = wallpaper.resize((width, height))

    new_image.paste(wallpaper, (0, 0))
    return new_image


class FileUtils:
    def __init__(self):
        pass

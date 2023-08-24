import os

from PIL import Image
from screeninfo import get_monitors

monitors = get_monitors()


def gen_img():
    width, height = monitors[0].width, monitors[0].height
    new_image = Image.new("RGB", (width, height), (0, 0, 0))

    wallpaper = Image.open(os.getcwd() + '/src/ressources/fantasy-2750995_1920.jpeg')
    wallpaper = wallpaper.resize((width, height))

    new_image.paste(wallpaper, (0, 0))
    return new_image


class FileUtils:
    def __init__(self):
        pass

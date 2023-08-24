import ctypes
import subprocess
import os

project_path = os.getcwd() + '/src/powerfullbackground/'
image_path = project_path + 'ressources/final.jpeg'


def set_xfce_wallpaper():
    screens = subprocess.check_output(['xfconf-query', '-c', 'xfce4-desktop', '-l']).decode().splitlines()

    # Set the wallpaper for each monitor and workspace
    for screen in screens:
        if 'last-image' in screen:
            subprocess.run(['xfconf-query', '-c', 'xfce4-desktop', '-p', screen, '-s', image_path])


def set_gnome_wallpaper():
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + image_path])


def set_windows_wallpaper():
    windows_path = os.path.abspath(image_path)

    # Set the wallpaper using the SystemParametersInfo function from the Windows API
    SPI_SETDESKWALLPAPER = 0x0014
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, windows_path, 3)

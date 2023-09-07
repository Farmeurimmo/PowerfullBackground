import ctypes
import os
import subprocess

image_path = os.path.join(os.getcwd(), 'src', 'powerfullbackground', 'ressources', 'final.jpeg')

SPI_SETDESKWALLPAPER = 20


def set_xfce_wallpaper():
    try:
        os.environ['DISPLAY'] = ':0'
        output = subprocess.check_output(['xfconf-query', '-c', 'xfce4-desktop', '-l'], stderr=subprocess.STDOUT)
        screens = output.decode('utf-8').split('\n')
    except subprocess.CalledProcessError as e:
        print(f"Command returned non-zero exit status {e.returncode}: {e.output.decode('utf-8')}")
        return

    # Set the wallpaper for each monitor and workspace
    for screen in screens:
        if 'last-image' in screen:
            subprocess.run(['sudo', 'xfconf-query', '-c', 'xfce4-desktop', '-p', screen, '-s', image_path])


def set_gnome_wallpaper():
    subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + image_path])


def set_windows_wallpaper():
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)


def set_mac_wallpaper():
    subprocess.run(
        ['osascript', '-e', 'tell application "Finder" to set desktop picture to POSIX file "' + image_path + '"'])

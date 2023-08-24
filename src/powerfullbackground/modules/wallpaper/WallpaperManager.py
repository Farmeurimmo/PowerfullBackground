import os
import subprocess

project_path = os.getcwd() + '/src/powerfullbackground/'
image_path = project_path + 'ressources/final.jpeg'


def set_xfce_wallpaper():
    try:
        os.environ['DISPLAY'] = ':0'
        output = subprocess.check_output(['xfconf-query', '-c', 'xfce4-desktop', '-l'], stderr=subprocess.STDOUT)
        print(output.decode('utf-8'))
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

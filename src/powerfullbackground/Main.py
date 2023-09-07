import platform

from modules.metrics.FileUtils import *
from modules.metrics.MetricVisualizer import *
from modules.metrics.SystemMetrics import *
from modules.wallpaper.WallpaperManager import *

interval = 0.5  # seconds

project_path = os.getcwd() + '/src/powerfullbackground/'

file_name = project_path + 'ressources/final.jpeg'

print('Starting PowerfullBackground')


def get_os():
    return platform.system()


def get_desktop_environment():
    if get_os().__contains__('Windows'):
        return 'windows'
    if get_os().__contains__('Mac'):
        return 'mac'
    desktop_session = os.environ.get('DESKTOP_SESSION')
    if desktop_session:
        desktop_session = desktop_session.lower()
        if 'xfce' in desktop_session:
            return 'xfce'
        elif 'gnome' in desktop_session:
            return 'gnome'
    return None


os_env = get_desktop_environment()
print(os_env)


def apply_wallpaper():
    if os_env == 'windows':
        set_windows_wallpaper()
    elif os_env == 'xfce':
        set_xfce_wallpaper()
    elif os_env == 'gnome':
        set_gnome_wallpaper()
    elif os_env == 'mac':
        set_mac_wallpaper()


while True:
    print('Generating image')
    start_time = time.time()
    ram_usage, ram_total, ram_used, ram_free = SystemMetrics.get_ram_values()
    cpu_usage_percent, cpu_frequency = SystemMetrics.get_cpu_values()
    network_sent, network_recv = SystemMetrics.get_network_values()
    read_bytes, write_bytes = SystemMetrics.get_disk_io_values()

    img = gen_img()
    if img is None:
        print('Error generating image')
        time.sleep(interval / 2)
        continue

    gen_cpu_bar(img, 10, 10, cpu_usage_percent, cpu_frequency)
    gen_ram_bar(img, 10, 60, ram_usage, ram_used)
    gen_network_bar(img, 10, 150, network_sent, network_recv)
    gen_disk_io_bar(img, 10, 200, read_bytes, write_bytes)

    img.save(file_name, format='JPEG')

    apply_wallpaper()

    took = time.time() - start_time
    print('took: ' + str(took) + 's')
    if interval - took > 0:
        time.sleep(interval - took)

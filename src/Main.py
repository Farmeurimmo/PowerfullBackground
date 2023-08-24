import subprocess

from src.modules.metrics.MetricVisualizer import *
from src.modules.metrics.SystemMetrics import *
from utils.FileUtils import *

interval = 0.4  # seconds

project_path = os.getcwd() + '/src/'

file_name = project_path + 'ressources/final.jpeg'


def set_wallpaper():
    image_path = project_path + 'ressources/final.jpeg'
    cmd = f'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitoreDP-1/workspace0/last-image -s "{image_path}"'
    subprocess.run(cmd, shell=True)


while True:
    start_time = time.time()
    cpu_usage_percent, cpu_frequency = get_cpu()
    ram_usage, ram_total, ram_used, ram_free = get_ram()
    network_sent, network_recv = get_network()
    read_bytes, write_bytes = get_disk_io()

    img = gen_img()

    gen_cpu_bar(img, 10, 10, cpu_usage_percent, cpu_frequency)
    gen_ram_bar(img, 10, 60, ram_usage, ram_used)
    gen_network_bar(img, 10, 150, network_sent, network_recv)
    gen_disk_io_bar(img, 10, 200, read_bytes, write_bytes)

    img.save(file_name, format='JPEG')

    set_wallpaper()

    took = time.time() - start_time
    if interval - took > 0:
        time.sleep(interval - took)

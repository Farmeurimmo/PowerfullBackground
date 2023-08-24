from modules.metrics.FileUtils import *
from modules.metrics.MetricVisualizer import *
from modules.metrics.SystemMetrics import *
from modules.wallpaper.WallpaperManager import *

interval = 0.4  # seconds

project_path = os.getcwd() + '/src/powerfullbackground/'

file_name = project_path + 'ressources/final.jpeg'

print('Starting PowerfullBackground')

while True:
    print('Generating image')
    start_time = time.time()
    cpu_usage_percent, cpu_frequency = get_cpu()
    ram_usage, ram_total, ram_used, ram_free = get_ram()
    network_sent, network_recv = get_network()
    read_bytes, write_bytes = get_disk_io()

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

    set_xfce_wallpaper()

    took = time.time() - start_time
    print('took: ' + str(took) + 's')
    if interval - took > 0:
        time.sleep(interval - took)

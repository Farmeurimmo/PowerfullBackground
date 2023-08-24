import os
import subprocess
import time

import cpuinfo
import psutil
from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors

monitors = get_monitors()

interval = 0.4  # seconds

network_last_in = 0
network_last_out = 0

disk_io_last_read = 0
disk_io_last_write = 0

last_time_took_to_update = time.time()

file_name = 'final.jpeg'

background_color = (52, 36, 32)

fill_free = (0, 255, 0)
fill_used = (255, 0, 0)

font = ImageFont.truetype("polices/arial.ttf", 30)


def draw_rectangle(image, coords, outline, width, fill):
    draw = ImageDraw.Draw(image)
    draw.rectangle(coords, outline=outline, width=width, fill=fill)

    return image


def draw_triangle(image, coords, outline, width, fill):
    draw = ImageDraw.Draw(image)
    draw.polygon(coords, outline=outline, width=width, fill=fill)

    return image


def draw_circle(image, coords, outline, width, fill):
    draw = ImageDraw.Draw(image)
    draw.ellipse(coords, outline=outline, width=width, fill=fill)

    return image


def draw_line(image, coords, fill, width):
    draw = ImageDraw.Draw(image)
    draw.line(coords, fill=fill, width=width)

    return image


def write_text(image, text, coords, font, fill):
    draw = ImageDraw.Draw(image)
    draw.text(coords, text, font=font, fill=fill)

    return image


def gen_img():
    width, height = monitors[0].width, monitors[0].height
    new_image = Image.new("RGB", (width, height), background_color)

    wallpaper = Image.open('fantasy-2750995_1920.jpeg')
    wallpaper = wallpaper.resize((width, height))

    new_image.paste(wallpaper, (0, 0))
    return new_image


def get_cpu():
    cpu_usage_percent = psutil.cpu_percent(interval=0)

    cpu_info = cpuinfo.get_cpu_info()
    cpu_frequency = cpu_info['hz_actual_friendly'].replace(' GHz', '')
    cpu_frequency = round(float(cpu_frequency), 2)

    return cpu_usage_percent, cpu_frequency


def get_ram():
    ram = psutil.virtual_memory()
    ram_total = ram.total / (1024 ** 3)
    ram_used = round((ram.total - ram.available) / (1024 ** 3), 2)
    ram_percent = ram.percent
    ram_free = ram.available / (1024 ** 3)
    return ram_percent, ram_total, ram_used, ram_free


def get_network():
    network = psutil.net_io_counters()
    global network_last_in
    global network_last_out
    global last_time_took_to_update

    current_time = time.time()
    time_diff = current_time - last_time_took_to_update

    # Calculate the transfer rate in Mbps
    network_in_calc = (network.bytes_recv - network_last_in) * 8 / (1024 ** 2 * time_diff)
    network_out_calc = (network.bytes_sent - network_last_out) * 8 / (1024 ** 2 * time_diff)

    # Update the last values and time
    network_last_in = network.bytes_recv
    network_last_out = network.bytes_sent
    last_time_took_to_update = current_time

    return round(network_in_calc, 2), round(network_out_calc, 2)


def get_disk_io():
    disk_io = psutil.disk_io_counters()

    global disk_io_last_read
    global disk_io_last_write
    global last_time_took_to_update

    current_time = time.time()
    time_diff = current_time - last_time_took_to_update

    # Calculate the transfer rate
    disk_io_read_calc = (disk_io.read_bytes - disk_io_last_read) / (1024 ** 2 * time_diff)
    disk_io_write_calc = (disk_io.write_bytes - disk_io_last_write) / (1024 ** 2 * time_diff)

    # convert to Mo/s
    disk_io_read_calc = disk_io_read_calc / 1024
    disk_io_write_calc = disk_io_write_calc / 1024

    # Update the last values and time
    disk_io_last_read = disk_io.read_bytes
    disk_io_last_write = disk_io.write_bytes
    last_time_took_to_update = current_time

    return round(disk_io_read_calc, 2), round(disk_io_write_calc, 2)


def set_wallpaper():
    image_path = os.path.join(os.getcwd(), 'final.jpeg')
    cmd = f'xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitoreDP-1/workspace0/last-image -s "{image_path}"'
    subprocess.run(cmd, shell=True)


def gen_cpu_bar(img, x, y, cpu_usage_percent, cpu_frequency):
    bar_width = 1000
    bar_height = 40
    outline = 'white'
    fill = (255, 0, 0)
    draw_until = int(bar_width * cpu_usage_percent / 100)
    # draw_rectangle(img, [(x, y), (x + bar_width, y + bar_height)], fill_free, 0, fill_free)
    draw_rectangle(img, [(x, y), (x + draw_until, y + bar_height)], fill, 0, fill)
    draw_rectangle(img, [(x, y), (x + bar_width, y + bar_height)], outline, 1, None)
    write_text(img, f'{cpu_usage_percent}%', (x + bar_width + 20, y), font, (255, 255, 255))
    write_text(img, f'{cpu_frequency} GHz', (x + bar_width + 20 + 100, y), font, (255, 255, 255))


def gen_ram_bar(img, x, y, ram_usage, ram_used):
    bar_width = 1000
    bar_height = 40
    outline = 'white'
    draw_until = int(bar_width * ram_usage / 100)
    # draw_rectangle(img, [(x, y), (x + bar_width, y + bar_height)], fill_free, 0, fill_free)
    draw_rectangle(img, [(x, y), (x + draw_until, y + bar_height)], fill_used, 0, fill_used)
    draw_rectangle(img, [(x, y), (x + bar_width, y + bar_height)], outline, 1, None)
    write_text(img, f'{ram_usage}%', (x + bar_width + 20, y), font, (255, 255, 255))
    write_text(img, f'{ram_used} GB', (x + bar_width + 20 + 100, y), font, (255, 255, 255))


def gen_network_bar(img, x, y, network_sent, network_recv):
    arrow_width = 40
    arrow_height = 40
    arrow_x = x
    arrow_y = y
    arrow_fill = (0, 0, 255)
    arrow_y -= 35
    write_text(img, 'Network', (arrow_x, arrow_y), font, (255, 255, 255))
    arrow_x += 150
    arrow_y += 35
    arrow_coords = [(arrow_x, arrow_y), (arrow_x + arrow_width, arrow_y),
                    (arrow_x + arrow_width / 2, arrow_y - arrow_height)]
    draw_triangle(img, arrow_coords, None, 1, arrow_fill)
    arrow_y -= 35
    write_text(img, f'{network_sent} Mbps', (arrow_x + arrow_width + 20, arrow_y), font, (255, 255, 255))
    arrow_x += 270
    arrow_fill = (255, 0, 255)
    arrow_coords = [(arrow_x, arrow_y), (arrow_x + arrow_width, arrow_y),
                    (arrow_x + arrow_width / 2, arrow_y + arrow_height)]
    draw_triangle(img, arrow_coords, None, 1, arrow_fill)
    write_text(img, f'{network_recv} Mbps', (arrow_x + arrow_width + 20, arrow_y), font, (255, 255, 255))


def gen_disk_io_bar(img, x, y, read_bytes, write_bytes):
    arrow_width = 40
    arrow_height = 40
    arrow_x = x
    arrow_y = y
    arrow_fill = (0, 127, 255)
    arrow_y -= 35
    write_text(img, 'Disk IO', (arrow_x, arrow_y), font, (255, 255, 255))
    arrow_x += 150
    arrow_y += 35
    arrow_coords = [(arrow_x, arrow_y), (arrow_x + arrow_width, arrow_y),
                    (arrow_x + arrow_width / 2, arrow_y - arrow_height)]
    draw_triangle(img, arrow_coords, None, 1, arrow_fill)
    arrow_y -= 35
    write_text(img, f'{read_bytes} Mo/s', (arrow_x + arrow_width + 20, arrow_y), font, (255, 255, 255))
    arrow_x += 270
    arrow_fill = (200, 96, 255)
    arrow_coords = [(arrow_x, arrow_y), (arrow_x + arrow_width, arrow_y),
                    (arrow_x + arrow_width / 2, arrow_y + arrow_height)]
    draw_triangle(img, arrow_coords, None, 1, arrow_fill)
    write_text(img, f'{write_bytes} Mo/s', (arrow_x + arrow_width + 20, arrow_y), font, (255, 255, 255))


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

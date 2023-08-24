import os

from PIL import ImageFont

from src.utils.ShapeDrawerUtils import *

font = ImageFont.truetype(os.getcwd() + '/src/ressources/polices/arial.ttf', 30)

fill_free = (0, 255, 0)
fill_used = (255, 0, 0)


def gen_cpu_bar(img, x, y, cpu_usage_percent, cpu_frequency):
    bar_width = 1000
    bar_height = 40
    outline = 'white'
    fill = (255, 0, 0)
    draw_until = int(bar_width * cpu_usage_percent / 100)
    draw_rectangle(img, [(x, y), (x + draw_until, y + bar_height)], fill, 0, fill)
    draw_rectangle(img, [(x, y), (x + bar_width, y + bar_height)], outline, 1, None)
    write_text(img, f'{cpu_usage_percent}%', (x + bar_width + 20, y), font, (255, 255, 255))
    write_text(img, f'{cpu_frequency} GHz', (x + bar_width + 20 + 100, y), font, (255, 255, 255))


def gen_ram_bar(img, x, y, ram_usage, ram_used):
    bar_width = 1000
    bar_height = 40
    outline = 'white'
    draw_until = int(bar_width * ram_usage / 100)
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

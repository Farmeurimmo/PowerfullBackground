import time

import cpuinfo
import psutil

network_last_in = 0
network_last_out = 0

disk_io_last_read = 0
disk_io_last_write = 0

last_time_took_to_update = time.time()


def get_cpu():
    cpu_usage_percent = psutil.cpu_percent(interval=0)

    cpu_info = cpuinfo.get_cpu_info()
    cpu_frequency = cpu_info['hz_actual_friendly'].replace(' GHz', '').replace(' MHz', '')
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

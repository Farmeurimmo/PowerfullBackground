import threading
import time

import cpuinfo
import psutil

disk_io_last_read = 0
disk_io_last_write = 0
last_time_took_to_update = 0
network_last_in = 0
network_last_out = 0


class SystemMetrics:
    cpu_usage_percent = 0
    cpu_frequency = 0
    ram_percent = 0
    ram_total = 0
    ram_used = 0
    ram_free = 0
    network_in = 0
    network_out = 0
    disk_io_read = 0
    disk_io_write = 0

    @classmethod
    def update_metrics(cls):
        while True:
            cls.cpu_usage_percent, cls.cpu_frequency = cls.get_cpu()
            cls.ram_percent, cls.ram_total, cls.ram_used, cls.ram_free = cls.get_ram()
            cls.network_in, cls.network_out = cls.get_network()
            cls.disk_io_read, cls.disk_io_write = cls.get_disk_io()
            time.sleep(0.4)

    @staticmethod
    def get_cpu():
        cpu_usage_percent = psutil.cpu_percent(interval=0)

        cpu_info = cpuinfo.get_cpu_info()
        cpu_frequency = cpu_info['hz_actual_friendly'].replace(' GHz', '').replace(' MHz', '')
        cpu_frequency = round(float(cpu_frequency), 2)

        return cpu_usage_percent, cpu_frequency

    @staticmethod
    def get_cpu_values():
        return SystemMetrics.cpu_usage_percent, SystemMetrics.cpu_frequency

    @staticmethod
    def get_ram():
        ram = psutil.virtual_memory()
        ram_total = ram.total / (1024 ** 3)
        ram_used = round((ram.total - ram.available) / (1024 ** 3), 2)
        ram_percent = ram.percent
        ram_free = ram.available / (1024 ** 3)

        return ram_percent, ram_total, ram_used, ram_free

    @staticmethod
    def get_ram_values():
        return SystemMetrics.ram_percent, SystemMetrics.ram_total, SystemMetrics.ram_used, SystemMetrics.ram_free

    @staticmethod
    def get_network():
        network = psutil.net_io_counters()

        global network_last_in, network_last_out, last_time_took_to_update

        current_time = time.time()
        time_diff = current_time - last_time_took_to_update
        if time_diff == 0:
            time_diff = 1

        # Calculate the transfer rate in Mbps
        network_in_calc = (network.bytes_recv - network_last_in) * 8 / (1024 ** 2 * time_diff)
        network_out_calc = (network.bytes_sent - network_last_out) * 8 / (1024 ** 2 * time_diff)

        # Update the last values and time
        network_last_in = network.bytes_recv
        network_last_out = network.bytes_sent
        last_time_took_to_update = current_time

        return round(network_in_calc, 2), round(network_out_calc, 2)

    @staticmethod
    def get_network_values():
        return SystemMetrics.network_in, SystemMetrics.network_out

    @staticmethod
    def get_disk_io():
        disk_io = psutil.disk_io_counters()

        global disk_io_last_read, disk_io_last_write, last_time_took_to_update

        current_time = time.time()
        time_diff = current_time - last_time_took_to_update
        if time_diff == 0:
            time_diff = 1

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

    @staticmethod
    def get_disk_io_values():
        return SystemMetrics.disk_io_read, SystemMetrics.disk_io_write


def run_metrics():
    SystemMetrics.update_metrics()


# Example usage
background_thread = threading.Thread(target=run_metrics)
background_thread.daemon = True
background_thread.start()

# Continue executing other tasks or code
print("Main thread continues executing")

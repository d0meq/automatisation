import psutil
import time

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'free': mem.free,
        'percent': mem.percent
    }

def get_disk_usage():
    partitions = psutil.disk_partitions()
    disk_usage = {}
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage[partition.mountpoint] = {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            }
        except PermissionError:
            # Ignore partitions that user does not have permission to access
            pass
    return disk_usage

def get_network_stats():
    stats = psutil.net_io_counters()
    return {
        'bytes_sent': stats.bytes_sent,
        'bytes_received': stats.bytes_recv,
        'packets_sent': stats.packets_sent,
        'packets_received': stats.packets_recv
    }

def monitor_system(interval=5):
    while True:
        print("=" * 40)
        print("CPU Usage: {}%".format(get_cpu_usage()))
        print("Memory Usage:", get_memory_usage())
        print("Disk Usage:", get_disk_usage())
        print("Network Stats:", get_network_stats())
        print("=" * 40)
        time.sleep(interval)

if __name__ == "__main__":
    monitor_system()
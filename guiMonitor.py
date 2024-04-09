import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psutil
import time

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.create_widgets()
        self.update_system_info()

    def create_widgets(self):
        self.label_cpu = ttk.Label(self.root, text="CPU Usage:")
        self.label_cpu.grid(row=0, column=0, sticky="w")

        self.label_memory = ttk.Label(self.root, text="Memory Usage:")
        self.label_memory.grid(row=1, column=0, sticky="w")

        self.label_disk = ttk.Label(self.root, text="Disk Usage:")
        self.label_disk.grid(row=2, column=0, sticky="w")

        self.label_network = ttk.Label(self.root, text="Network Stats:")
        self.label_network.grid(row=3, column=0, sticky="w")

        self.text_cpu = tk.Text(self.root, width=50, height=1, wrap="none")
        self.text_cpu.grid(row=0, column=1)

        self.text_memory = tk.Text(self.root, width=50, height=3, wrap="none")
        self.text_memory.grid(row=1, column=1)

        self.text_disk = tk.Text(self.root, width=50, height=3, wrap="none")
        self.text_disk.grid(row=2, column=1)

        self.text_network = tk.Text(self.root, width=50, height=2, wrap="none")
        self.text_network.grid(row=3, column=1)

    def update_system_info(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            network_stats = psutil.net_io_counters()

            self.text_cpu.delete('1.0', tk.END)
            self.text_cpu.insert(tk.END, f"{cpu_usage}%")

            self.text_memory.delete('1.0', tk.END)
            self.text_memory.insert(tk.END, f"Total: {self.format_bytes(memory_usage.total)}\n"
                                             f"Used: {self.format_bytes(memory_usage.used)}\n"
                                             f"Free: {self.format_bytes(memory_usage.free)}\n"
                                             f"Percent: {memory_usage.percent}%")

            self.text_disk.delete('1.0', tk.END)
            self.text_disk.insert(tk.END, f"Total: {self.format_bytes(disk_usage.total)}\n"
                                           f"Used: {self.format_bytes(disk_usage.used)}\n"
                                           f"Free: {self.format_bytes(disk_usage.free)}\n"
                                           f"Percent: {disk_usage.percent}%")

            self.text_network.delete('1.0', tk.END)
            self.text_network.insert(tk.END, f"Bytes Sent: {self.format_bytes(network_stats.bytes_sent)}\n"
                                              f"Bytes Received: {self.format_bytes(network_stats.bytes_recv)}\n"
                                              f"Packets Sent: {network_stats.packets_sent}\n"
                                              f"Packets Received: {network_stats.packets_recv}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.root.after(5000, self.update_system_info)  # Update every 5 seconds

    def format_bytes(self, bytes):
        # Format bytes to human-readable format
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if abs(bytes) < 1024.0:
                return "%3.1f%sB" % (bytes, unit)
            bytes /= 1024.0
        return "%.1f%sB" % (bytes, 'E')


if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.create_widgets()
        self.update_system_info()
        self.create_graphs()

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

        self.graph_frame = ttk.LabelFrame(self.root, text="System Usage Graphs")
        self.graph_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def create_graphs(self):
        self.fig, self.ax = plt.subplots(2, 2, figsize=(10, 6))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5)
        self.ax = self.ax.ravel()

        self.ax[0].set_title('CPU Usage (%)')
        self.ax[0].set_xlabel('Time (s)')
        self.ax[0].set_ylabel('CPU Usage')
        self.ax[0].set_ylim(0, 100)
        self.ax[0].set_xlim(0, 30)
        self.cpu_line, = self.ax[0].plot([], [], lw=2)  # Moved here

        self.ax[1].set_title('Memory Usage (%)')
        self.ax[1].set_xlabel('Time (s)')
        self.ax[1].set_ylabel('Memory Usage')
        self.ax[1].set_ylim(0, 100)
        self.ax[1].set_xlim(0, 30)
        self.memory_line, = self.ax[1].plot([], [], lw=2)  # Moved here

        self.ax[2].set_title('Disk Usage (%)')
        self.ax[2].set_xlabel('Time (s)')
        self.ax[2].set_ylabel('Disk Usage')
        self.ax[2].set_ylim(0, 100)
        self.ax[2].set_xlim(0, 30)
        self.disk_line, = self.ax[2].plot([], [], lw=2)  # Moved here

        self.ax[3].set_title('Network Usage (Bytes)')
        self.ax[3].set_xlabel('Time (s)')
        self.ax[3].set_ylabel('Network Usage')
        self.ax[3].set_xlim(0, 30)
        self.bytes_sent_line, = self.ax[3].plot([], [], label='Bytes Sent', lw=2)  # Moved here
        self.bytes_received_line, = self.ax[3].plot([], [], label='Bytes Received', lw=2)  # Moved here
        self.ax[3].legend(loc='upper right')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=tk.YES)

    def update_system_info(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            network_stats = psutil.net_io_counters()

            self.text_cpu.delete('1.0', tk.END)
            self.text_cpu.insert(tk.END, f"{cpu_usage}%")

            self.text_memory.delete('1.0', tk.END)
            self.text_memory.insert(tk.END, f"{memory_usage}%")

            self.text_disk.delete('1.0', tk.END)
            self.text_disk.insert(tk.END, f"{disk_usage}%")

            self.text_network.delete('1.0', tk.END)
            self.text_network.insert(tk.END, f"Bytes Sent: {self.format_bytes(network_stats.bytes_sent)}\n"
                                              f"Bytes Received: {self.format_bytes(network_stats.bytes_recv)}\n"
                                              f"Packets Sent: {network_stats.packets_sent}\n"
                                              f"Packets Received: {network_stats.packets_recv}")

            self.update_graphs(cpu_usage, memory_usage, disk_usage, network_stats.bytes_sent, network_stats.bytes_recv)

        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.root.after(5000, self.update_system_info)  # Update every 5 seconds

    def update_graphs(self, cpu_usage, memory_usage, disk_usage, bytes_sent, bytes_received):
        x = np.arange(0, 30)
        self.cpu_line.set_data(x, [cpu_usage]*30)
        self.memory_line.set_data(x, [memory_usage]*30)
        self.disk_line.set_data(x, [disk_usage]*30)
        self.bytes_sent_line.set_data(x, [bytes_sent]*30)
        self.bytes_received_line.set_data(x, [bytes_received]*30)

        for ax in self.ax:
            ax.relim()
            ax.autoscale_view()
        self.fig.canvas.draw()

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
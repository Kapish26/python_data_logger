"""
    Module to create a simple UI for CSU serial port communication.
"""

from utils import resource_path
from constants import NUM_THERMISTORS, NUM_NETWORKS
from serial_communicator import SerialCommunicator
from menu import CsuMenu
from serial.tools.list_ports import comports
import serial
import ttkbootstrap as ttk
import numpy as np
from queue import Queue
from threading import Thread
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import Toplevel, messagebox, Menu, Tk
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
import tkinter as tk
import random
import matplotlib
matplotlib.use('TkAgg')


class SerialUI:
    """
        Class to create a simple UI for serial port communication
    """

    def __init__(self):
        self.root = Tk()  # Create the main window object
        # Set the window title bar text
        self.root.title("Data Logger")
        self.serial_communicator = None  # SerialCommunicator object initialization
        self.ports = []  # List to hold available serial ports
        self.solenoid_cutoff = tk.IntVar(value=10)
        self.repetition_rate = tk.DoubleVar(value=0.1)
        self.heater_activation = tk.IntVar(value=10)
        self.cooling_enabled = tk.BooleanVar(value=True)
        self.wifi_ssids = [tk.StringVar() for _ in range(NUM_NETWORKS)]
        self.wifi_passwords = [tk.StringVar() for _ in range(NUM_NETWORKS)]

        CsuMenu(self)  # Create the menu bar

        # Get available serial ports
        self.get_serial_ports()

        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(padx=10, pady=10, anchor='w')
        # Serial Port Selection Section UI
        self.serial_ports_container = ttk.Frame(self.header_frame)
        self.serial_ports_container.grid(row=0, column=0)
        self.serial_label = ttk.Label(
            self.serial_ports_container, text="Select Serial Port:")
        self.serial_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        # Refresh Button
        self.refresh_icon = Image.open(resource_path("refresh_icon.png"))
        self.refresh_icon = self.refresh_icon.resize(
            (16, 16), Image.LANCZOS)  # type: ignore # Resize the icon as needed
        self.refresh_icon = ImageTk.PhotoImage(
            self.refresh_icon)  # Convert to PhotoImage
        self.refresh_button = ttk.Button(
            self.serial_ports_container, image=self.refresh_icon, command=self.refresh_ports,)  # type: ignore
        self.refresh_button.grid(row=0, column=1, padx=5, sticky='w')

        self.selected_port = tk.StringVar()  # Variable to hold selected port

        # Create radio buttons for each available port
        for i, port in enumerate(self.ports):
            rb = ttk.Radiobutton(
                self.serial_ports_container,
                text=port['description'],
                variable=self.selected_port,
                value=port['device'],
                command=self.close_serial,
            )
            rb.grid(row=i+1, padx=5, pady=2, sticky='w')

        # Button Frame
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Open Port Button
        self.open_button = ttk.Button(
            self.button_frame, text="Open Port", command=self.open_serial, )
        self.open_button.grid(row=0, column=0, padx=5)

        # Close Port Button
        self.close_button = ttk.Button(
            self.button_frame, text="Close Port", command=self.close_serial, state="disabled",)
        self.close_button.grid(row=0, column=1, padx=5)

        # Create a frame to hold both the thermistor data and the plot
        self.data_plot_frame = ttk.Frame(self.root)
        self.data_plot_frame.pack(pady=10)

        # Create a sub-frame for thermistor data
        self.thermistor_data_frame = ttk.Frame(self.data_plot_frame)
        self.thermistor_data_frame.grid(
            row=0, column=0, padx=10, pady=5, sticky='nw')

        self.live_thermistor_data = []

        self.create_live_thermistor_data()

        self.create_live_matplotlib_data()

        self.display_thermistor_checkboxes()

        # Received Data Display
        self.received_data_frame = ttk.Frame(self.root)
        self.received_data_frame.pack(pady=10)
        self.scrollbar = ttk.Scrollbar(
            self.received_data_frame, orient='vertical')
        self.scrollbar.grid(row=1, column=2, sticky='nsw')

        self.received_data_text = tk.Text(
            self.received_data_frame, width=80, height=10, yscrollcommand=self.scrollbar.set, state="disabled")
        self.received_data_text.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky='w')
        self.scrollbar.config(command=self.received_data_text.yview)

        # Queue for communication between threads
        self.queue = Queue()

        self.root.mainloop()

    def create_live_thermistor_data(self):

        for i in range(NUM_THERMISTORS):
            column = 1 if i % 2 else 0
            row = i // 2
            thermistor_label = ttk.Label(self.thermistor_data_frame,
                                         text=f"T{i+1}:")
            thermistor_label.grid(
                row=row * 2, column=column, padx=10, pady=5, sticky='w')
            thermistor_entry = ttk.Entry(
                self.thermistor_data_frame, width=20, state="disabled")
            thermistor_entry.grid(row=row * 2 + 1, column=column,
                                  padx=10, pady=5, sticky='w')
            thermistor_entry.config(state="disabled")
            self.live_thermistor_data.append(thermistor_entry)

    def display_thermistor_checkboxes(self):
        self.checkbox_frame = ttk.Frame(self.data_plot_frame)
        self.checkbox_frame.grid(row=0, column=1, padx=10, pady=5, sticky='nw')

        self.thermistor_vars = []
        for i in range(16):
            var = tk.BooleanVar(value=True)
            checkbox = ttk.Checkbutton(
                self.checkbox_frame, text=f'T{i+1}', variable=var, command=self.update_plot,)
            checkbox.grid(row=0, column=i, padx=5, pady=5, sticky='w')
            self.thermistor_vars.append(var)

    def create_live_matplotlib_data(self):
        self.plot_frame = ttk.Frame(self.data_plot_frame)
        # Place it next to thermistor data
        self.plot_frame.grid(row=0, column=1, padx=10, pady=5, sticky='ne')

        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)

        # X-axis will represent time, initialize with an empty list
        self.time_data = []
        # Y-axis will represent temperature, initialize with 16 lists for 16 thermistors
        self.temp_data = [[] for _ in range(16)]

        self.lines = []  # To store the lines for each thermistor

        for i in range(16):
            line, = self.ax.plot([], [], label=f'T{i+1}')
            self.lines.append(line)

        self.ax.set_title('Temperature Data')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Temperature (K)')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ax.legend()
        self.start_time = None

    def update_data(self, timestamp: str, temps):
        try:
            current_time = datetime.strptime(f"{datetime.today().strftime(
                '%Y-%m-%d')} {timestamp.strip()}", "%Y-%m-%d %H:%M:%S")

            if self.start_time is None:
                self.start_time = current_time
                self.temp_time = current_time

            # Check if 'temps' contains valid temperature data
            if len(temps) == 16 and ((current_time - self.temp_time).total_seconds() >= self.repetition_rate.get() * 60):
                elapsed_time = current_time - self.start_time
                self.temp_time = current_time

                # Append timestamp to time_data
                self.time_data.append(elapsed_time.total_seconds())

                # Iterate over temperature data for each thermistor
                for i, temp in enumerate(temps):
                    # Append temperature data to temp_data for each thermistor
                    self.temp_data[i].append(float(temp))

                # Update the plot
                self.update_plot()

            else:
                # If 'temps' does not contain valid temperature data, print a message
                print("Invalid temperature data received.")

        except Exception as e:
            # Handle any exceptions that occur during the plotting process
            print(f"Error updating plot: {e}")

    def update_plot(self,):
        self.ax.clear()
        # Update each line
        for i, line in enumerate(self.lines):
            if self.thermistor_vars[i].get():
                self.ax.plot(self.time_data,
                             self.temp_data[i], label=f'T{i+1}')

        # Adjust y-axis limits
        min_temp = min([min(temp) for temp in self.temp_data])
        max_temp = max([max(temp) for temp in self.temp_data])
        # Adjust y-axis limits to accommodate the temperature range
        self.ax.set_ylim(min_temp - 1, max_temp + 1)

        self.ax.set_title('Temperature Data')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Temperature (K)')
        self.ax.legend()

        # Redraw the canvas to reflect the updated plot
        self.canvas.draw()

    def refresh_ports(self):
        """
        Refresh the list of available serial ports.
        """
        # Clear existing radio buttons
        for rb in self.serial_ports_container.grid_slaves():
            if isinstance(rb, ttk.Radiobutton):
                rb.grid_forget()

        # Get available serial ports
        self.get_serial_ports()

        # Create new radio buttons for each available port
        for i, (port) in enumerate(self.ports):
            rb = ttk.Radiobutton(
                self.serial_ports_container,
                text=port['description'],
                variable=self.selected_port,
                value=port['device'],
                command=self.close_serial,
            )
            rb.grid(row=i+1, padx=5, pady=2, sticky='w')

    def get_serial_ports(self):
        """
            Get a list of available serial ports.
        """
        try:
            ports = comports()
            ports = comports()
            self.ports = []
            for port in ports:
                port_info = {'device': port.device,
                             'description': port.description}
                self.ports.append(port_info)
                print(f"{port.description}: {port.device}")
        except serial.SerialException as e:
            print(f"Error listing serial ports: {e}")

    def open_serial(self):
        """
            Open the selected serial port.
        """
        port = self.selected_port.get()
        if port:
            self.received_data_text.config(state="normal")
            self.received_data_text.delete(1.0, tk.END)
            # Set focus to the text widget
            self.received_data_text.focus_set()
            # Update the scrollbar
            self.scrollbar.set(0.0, 1.0)
            self.received_data_text.config(state="disabled")
            self.serial_communicator = SerialCommunicator(port)
            if self.serial_communicator.open_serial_port():
                print(f"Serial port {port} opened successfully.")
                self.open_button.config(state="disabled")
                self.close_button.config(state="normal")
                # Start reading thread
                self.read_thread = Thread(target=self.read_serial_thread)
                self.read_thread.daemon = True
                self.read_thread.start()

            else:
                print(f"Failed to open serial port {port}.")

    def close_serial(self):
        """
            Close the serial port.
        """
        if self.serial_communicator:
            self.serial_communicator.close_serial_port()
            self.received_data_text.delete(1.0, tk.END)
            # Set focus to the text widget
            self.received_data_text.focus_set()
            # Update the scrollbar
            self.scrollbar.set(0.0, 1.0)

            self.open_button.config(state="normal")
            self.close_button.config(state="disabled")
            self.serial_communicator = None

            for window in self.root.winfo_children():
                if window.winfo_class() == 'Toplevel':
                    window.destroy()

            print("Serial port closed.")

    def read_serial_thread(self):
        """
            Thread to read data from the serial port.
        """
        counter = 0
        while True:
            if self.serial_communicator:
                try:
                    received_data = self.serial_communicator.read_from_serial()

                    if received_data.startswith("Live:"):
                        data = received_data.split(":")[1].split(";")
                        live_data_timestamp = data[0]
                        live_data_timestamp = live_data_timestamp.replace(
                            ".", ":")
                        live_data = data[1].split(",")
                        if len(live_data) == 16:  # Ensure there are 16 temperature values
                            # Update the plot
                            self.update_data(live_data_timestamp, live_data)
                        for i, entry in enumerate(self.live_thermistor_data):
                            entry.config(state="normal")
                            entry.delete(0, tk.END)
                            entry.insert(0, live_data[i])
                            entry.config(state="disabled")
                    elif received_data.startswith("Wifi Credentials:"):
                        data = received_data.split(":")[1].split(";")
                        for i, entry in enumerate(data):
                            ssid, password = entry.split(",")
                            self.wifi_ssids[i].set(ssid)
                            self.wifi_passwords[i].set(password)
                    elif received_data.startswith("Cooling Enabled:"):
                        data = received_data.split(":")[1]
                        self.cooling_enabled.set(data == "1")
                    elif received_data.startswith("Solenoid Cutoff Temperature:"):
                        data = received_data.split(":")[1]
                        self.solenoid_cutoff.set(int(data))
                    elif received_data.startswith("Heater Activation Temperature:"):
                        data = received_data.split(":")[1]
                        self.heater_activation.set(int(data))
                    else:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
                        # Check if the user has manually scrolled
                        manual_scroll = self.received_data_text.yview()[
                            1] != 1.0
                        self.received_data_text.config(state="normal")
                        self.received_data_text.insert(
                            tk.END, f"[{timestamp}] {received_data}" + "\n")
                        self.received_data_text.config(state="disabled")
                        if not manual_scroll:
                            self.received_data_text.see(tk.END)
                        self.root.update()
                        if received_data:
                            self.queue.put(received_data)
                except Exception as e:
                    print(f"Error reading data: {e}")
                    self.received_data_text.delete(1.0, tk.END)
                    self.close_serial()
                    self.refresh_ports()
                    break
            else:
                break
            # time.sleep(0.1)

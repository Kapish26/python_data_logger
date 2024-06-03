"""
    Module to create a simple UI for CSU serial port communication.
"""

from queue import Queue
from threading import Thread
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import Toplevel, messagebox, Menu, Tk

import ttkbootstrap as ttk
import tkinter as tk
import serial

from serial.tools.list_ports import comports

from menu import CsuMenu
from serial_communicator import SerialCommunicator

from constants import NUM_THERMISTORS

from utils import resource_path


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
            (16, 16), Image.LANCZOS)  # Resize the icon as needed
        self.refresh_icon = ImageTk.PhotoImage(
            self.refresh_icon)  # Convert to PhotoImage
        self.refresh_button = ttk.Button(
            self.serial_ports_container, image=self.refresh_icon, command=self.refresh_ports,)
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

        self.header_split = ttk.Separator(
            self.header_frame, orient='vertical')
        self.header_split.grid(row=0, column=3, sticky='ns', padx=10)

        self.cooling_enabled = tk.IntVar(value=0)

        # Cooling Enable
        self.cooling_enabled_frame = ttk.Frame(self.header_frame)
        self.cooling_enabled_frame.grid(row=0, column=4)
        self.cooling_enabled_button = ttk.Checkbutton(
            self.cooling_enabled_frame, text="Enable Slits", variable=self.cooling_enabled, state="disabled",)

        self.cooling_enabled_button.grid(row=0, column=0,
                                         padx=5, pady=5, sticky='w')
        self.enable_slits_button = ttk.Button(
            self.cooling_enabled_frame, text="Send", state="disabled")
        self.enable_slits_button.grid(
            row=0, column=1, padx=5, pady=5, sticky='w')

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

        # Data Logger Settings Frame
        self.data_logger_settings_frame = ttk.Frame(self.root)
        self.data_logger_settings_frame.pack(pady=10)

        #

        # Thermistor Data Frame
        self.thermistor_data_frame = ttk.Frame(self.root)
        self.thermistor_data_frame.pack(pady=10)

        self.live_thermistor_data = []

        self.create_live_thermistor_data()

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
            thermistor_label = ttk.Label(self.thermistor_data_frame,
                                         text=f"T{i+1}:")
            thermistor_label.grid(
                row=i*3, column=4, padx=10, pady=5, sticky='w')
            thermistor_entry = ttk.Entry(
                self.thermistor_data_frame, width=20, state="disabled")
            thermistor_entry.grid(row=i*3+1, column=4,
                                  padx=10, pady=5, sticky='w')
            self.live_thermistor_data.append(thermistor_entry)

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
                self.cooling_enabled_button.config(state="normal")

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
            self.cooling_enabled_button.config(state="disabled")
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
                        live_data = data[1].split(",")
                        for i, entry in enumerate(self.live_thermistor_data):
                            entry.config(state="normal")
                            entry.delete(0, tk.END)
                            entry.insert(0, live_data[i])
                            entry.config(state="disabled")
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

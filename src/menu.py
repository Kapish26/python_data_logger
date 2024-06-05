from tkinter import Menu, Toplevel, messagebox
import ttkbootstrap as ttk

from data_logger_settings import DataLoggerSettings
from serial_communicator import SerialCommunicator
from wifi_credentials import WifiCredentials


class CsuMenu:
    def __init__(self, parent):
        self.parent = parent
        self.root = parent.root

        # Creating Menubar
        self.menu = Menu(parent.root)
        self.root.config(menu=self.menu)  # Set the menu bar
        # Adding File Menu and commands
        self.file = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.file)
        self.file.add_command(label='Exit', command=parent.root.destroy)

        # Adding Edit Menu and commands
        self.edit = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Edit', menu=self.edit)
        self.edit.add_command(label='Edit Data Logger Settings',
                              command=self.open_data_logger_settings)
        self.edit.add_command(label='Edit WiFi Credentials',
                              command=self.open_wifi_credentials)

    def open_data_logger_settings(self):
        if self.parent.serial_communicator is None:
            messagebox.showerror(
                "Error", "Serial Communicator is not connected")
            return
        else:
            self.data_logger_settings = DataLoggerSettings(
                self.root, self.parent)

    def open_wifi_credentials(self):
        if self.parent.serial_communicator is None:
            messagebox.showerror(
                "Error", "Serial Communicator is not connected")
            return
        else:
            self.wifi_credentials = WifiCredentials(
                self.root, self.parent)

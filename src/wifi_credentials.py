from tkinter import Menu, Toplevel, messagebox
import ttkbootstrap as ttk

from data_logger_settings import DataLoggerSettings
from serial_communicator import SerialCommunicator

from constants import NUM_NETWORKS


class WifiCredentials:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.wifi_credentials_window = Toplevel(self.root)
        self.wifi_credentials_window.grab_set()
        self.wifi_credentials_window.title("WiFi Credentials")

        # WiFi Network Frame
        self.wifi_network_frame = ttk.Frame(self.wifi_credentials_window)
        self.wifi_network_frame.pack(pady=10)
        for i in range(NUM_NETWORKS):
            self.wifi_ssid_label = ttk.Label(
                self.wifi_network_frame, text=f"SSID {i + 1}:")
            self.wifi_ssid_label.grid(
                row=i*2, column=0, padx=2, pady=5, sticky='w')
            self.wifi_ssid_entry = ttk.Entry(
                self.wifi_network_frame, width=20, textvariable=self.parent.wifi_ssids[i])
            self.wifi_ssid_entry.grid(
                row=i*2 + 1, column=0, padx=2, pady=5, sticky='w')

            self.wifi_password_label = ttk.Label(
                self.wifi_network_frame, text=f"Password {i + 1}:")
            self.wifi_password_label.grid(
                row=i*2, column=1, padx=5, pady=5, sticky='w')
            self.wifi_password_entry = ttk.Entry(
                self.wifi_network_frame, width=20, textvariable=self.parent.wifi_passwords[i])
            self.wifi_password_entry.grid(
                row=i*2 + 1, column=1, padx=5, pady=5, sticky='w')

        # Send WiFi Credentials Button
        self.send_wifi_credentials_button = ttk.Button(
            self.wifi_credentials_window, text="Send WiFi Credentials", command=self.send_wifi_credentials)
        self.send_wifi_credentials_button.pack(pady=10)

    def send_wifi_credentials(self):
        if self.parent.serial_communicator is None:
            messagebox.showerror(
                "Error", "Serial Communicator is not connected")
            return
        else:
            data = "Wifi Credentials:"
            for i in range(NUM_NETWORKS):
                ssid = self.parent.wifi_ssids[i].get()
                password = self.parent.wifi_passwords[i].get()
                data += f"{ssid},{password}"
                if i < NUM_NETWORKS - 1:
                    data += ";"
            self.parent.serial_communicator.write_to_serial(data)

            self.wifi_credentials_window.destroy()

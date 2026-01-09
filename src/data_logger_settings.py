from tkinter import Menu, Toplevel, messagebox
import ttkbootstrap as ttk

from serial_communicator import SerialCommunicator


class DataLoggerSettings:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.data_logger_settings_window = Toplevel(self.root)
        self.data_logger_settings_window.grab_set()
        self.data_logger_settings_window.title("Data Logger Settings")
        # Data Logger Settings Frame
        self.data_logger_settings_frame = ttk.Frame(
            self.data_logger_settings_window)
        self.data_logger_settings_frame.pack(pady=10)

        # Heater Activation Temperature Frame
        self.heater_activation_frame = ttk.Frame(
            self.data_logger_settings_frame)
        self.heater_activation_frame.grid(row=0, column=0, pady=4)

        self.heater_activation_label = ttk.Label(
            self.heater_activation_frame, text="Heater Activation Temperature(K):")
        self.heater_activation_label.grid(
            row=0, column=0, padx=2, pady=5, sticky='w')
        self.heater_activation_entry = ttk.Entry(
            self.heater_activation_frame, width=10, textvariable=self.parent.heater_activation)
        self.heater_activation_entry.grid(
            row=0, column=1, padx=2, pady=5, sticky='w')
        self.heater_activation_button = ttk.Button(
            self.heater_activation_frame, text="Send", command=self.send_heater_activation)
        self.heater_activation_button.grid(
            row=0, column=2, padx=5, pady=5, sticky='w')

        # Solenoid Cut-off Temperature Frame
        self.solenoid_cutoff_frame = ttk.Frame(
            self.data_logger_settings_frame)
        self.solenoid_cutoff_frame.grid(row=1, column=0, pady=4)

        self.solenoid_cutoff_label = ttk.Label(
            self.solenoid_cutoff_frame, text="Solenoid Cut-off Temperature(K):")
        self.solenoid_cutoff_label.grid(
            row=0, column=0, padx=5, pady=5, sticky='w')
        self.solenoid_cutoff_entry = ttk.Entry(
            self.solenoid_cutoff_frame, width=10, textvariable=self.parent.solenoid_cutoff)
        self.solenoid_cutoff_entry.grid(
            row=0, column=1, padx=5, pady=5, sticky='w')
        self.solenoid_cutoff_button = ttk.Button(
            self.solenoid_cutoff_frame, text="Send", command=self.send_solenoid_cutoff)
        self.solenoid_cutoff_button.grid(
            row=0, column=2, padx=5, pady=5, sticky='w')

        # Cooling Enable Frame
        self.cooling_enabled_frame = ttk.Frame(self.data_logger_settings_frame)
        self.cooling_enabled_frame.grid(
            row=0, column=2, padx=4, sticky='w')

        # Cooling Enabled Button
        self.cooling_enabled_button = ttk.Checkbutton(
            self.cooling_enabled_frame, text="Cooling Enabled", variable=self.parent.cooling_enabled,)

        self.cooling_enabled_button.grid(row=0, column=0,
                                         padx=5, pady=5, sticky='w')
        self.enable_slits_button = ttk.Button(
            self.cooling_enabled_frame, text="Send", command=self.send_cooling_enabled)
        self.enable_slits_button.grid(
            row=0, column=1, padx=5, pady=5, sticky='w')

        # Repetition Rate (for data logging) Frame
        self.repetition_rate_frame = ttk.Frame(self.data_logger_settings_frame)
        self.repetition_rate_frame.grid(row=1, column=2, padx=4, sticky='w')

        self.repetition_rate_label = ttk.Label(
            self.repetition_rate_frame, text="Refresh Rate (s):")
        self.repetition_rate_label.grid(
            row=0, column=0, padx=5, pady=5, sticky='w')
        self.repetition_rate_entry = ttk.Entry(
            self.repetition_rate_frame, width=10, textvariable=self.parent.refresh_rate)
        self.repetition_rate_entry.grid(
            row=0, column=1, padx=5, pady=5, sticky='w')

        # Dumping Rate Frame
        self.dumping_rate_frame = ttk.Frame(self.data_logger_settings_frame)
        self.dumping_rate_frame.grid(
            row=2, column=0, padx=4, pady=4, sticky='w')

        self.dumping_rate_label = ttk.Label(
            self.dumping_rate_frame, text="Dumping Rate (s):")
        self.dumping_rate_label.grid(
            row=0, column=0, padx=5, pady=5, sticky='w')
        self.dumping_rate_entry = ttk.Entry(
            self.dumping_rate_frame, width=10, textvariable=self.parent.dumping_rate)
        self.dumping_rate_entry.grid(
            row=0, column=1, padx=5, pady=5, sticky='w')

    def send_heater_activation(self):
        if self.parent.serial_communicator is None:
            messagebox.showerror(
                "Error", "Serial Communicator is not connected")
            return
        else:
            data = f"Heater Activation Temperature:{self.parent.heater_activation.get()}"
            self.parent.serial_communicator.write_to_serial(data)

    def send_solenoid_cutoff(self):
        if self.parent.serial_communicator is None:
            messagebox.showerror(
                "Error", "Serial Communicator is not connected")
            return
        else:
            data = f"Solenoid Cutoff Temperature: {self.parent.solenoid_cutoff.get()}"
            self.parent.serial_communicator.write_to_serial(data)

    def send_cooling_enabled(self):
        if self.parent.serial_communicator is None:
            messagebox.showerror(
                "Error", "Serial Communicator is not connected")
            return
        else:
            data = f"Cooling Enabled: {1 if self.parent.cooling_enabled.get() else 0}"
            self.parent.serial_communicator.write_to_serial(data)

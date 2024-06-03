"""
    Module to handle serial communication with the Arduino.
"""
import serial
from datetime import datetime

from constants import BAUD_RATE


class SerialCommunicator:
    """
        Class to handle serial communication with the Arduino.
    """

    def __init__(self, port):
        self.serial_port = port
        self.serial_connection = None

    def open_serial_port(self):
        """
            Open the serial port for communication.
        """
        try:
            self.serial_connection = serial.Serial(self.serial_port, BAUD_RATE)
            return True
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")
            return False

    def close_serial_port(self):
        """
            Close the serial port.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Closed serial port.")

    def write_to_serial(self, data):
        """
            Write data to the serial port.
        """
        if self.serial_connection and self.serial_connection.is_open:
            print(f"Writing to serial port: {data}")
            date = datetime.now().strftime("%d-%m-%Y")
            # Open the file in append mode
            with open(f'{date}-logs.txt', 'a') as file:
                # Get the current timestamp
                timestamp = datetime.now().strftime("[%d-%m-%Y %H:%M:%S] : ")
                # Write the timestamp to the file followed by a newline character
                file.write(timestamp + data + '\n')
            self.serial_connection.write(data.encode())

    def read_from_serial(self):
        """
            Read data from the serial port.
        """
        if self.serial_connection and self.serial_connection.is_open:
            return self.serial_connection.readline().decode().strip()
        return ""

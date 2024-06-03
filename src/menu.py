from tkinter import Menu, Toplevel, messagebox
import ttkbootstrap as ttk

from serial_communicator import SerialCommunicator


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

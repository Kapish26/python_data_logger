# Data Logger GUI

The Data Logger GUI project connects with the hardware (an ESP32 module) using serial communication and currently supports data from 16 thermistors. This application allows users to monitor and configure temperature settings via a graphical user interface built with Python.


## Table of Contents
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Usage](#usage)
  - [Creating an Executable](#creating-an-executable)

## Features

- **Temperature Control**: Set heater activation temperatures and solenoid cutoff temperatures.
- **Cooling Settings**: Enable or disable cooling settings.
- **Live Data Display**: Shows real-time thermistor data.
- **Real-Time Graph**: Displays a real-time graph of temperature variations over time.
- **WiFi Credentials Management**: Stores up to 8 WiFi SSIDs and passwords.

## Installation

### Prerequisites

- Python 3.x
- Optionally, a virtual environment

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Kapish26/python_data_logger
    cd python_data_logger
    ```

2. **Set up a virtual environment (optional but recommended)**:
    ```bash
    python -m venv env
    source env/bin/activate   # On Windows, use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install PyInstaller globally**:
    ```bash
    pip install pyinstaller
    ```

## Usage

1. **Open the App**:
    - Locate the `main.exe` file on your desktop and double-click to open the Data Logger app.

2. **Connect Serial Ports**:
    - Before interacting with the app's features, ensure that you establish a connection to the relevant serial ports. This might involve connecting any hardware components to your computer or configuring virtual serial ports if applicable.

3. **Live Data Graph**:
    - The data is plotted from the time the serial port is connected. You can show or hide the thermistors' lines in the graph.

4. **Edit Data Logger Settings**:
    - To change heater activation temperatures, solenoid cutoff temperatures, and enable or disable cooling settings, go to the menu bar, select "Edit," and then choose "Edit Data Logger Settings."

5. **Edit WiFi Credentials**:
    - To store or edit WiFi SSIDs and passwords, go to the menu bar, select "Edit," and then choose "Edit WiFi Credentials." You can store up to 8 WiFi networks.

## Creating an Executable

To create an executable file that will run on Windows, use PyInstaller:

```bash
pyinstaller --onefile --add-data "refresh_icon.png:." src\main.py
```

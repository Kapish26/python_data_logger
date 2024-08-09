# Data Logger GUI

The Data Logger GUI project connects with the hardware (an ESP32 module) using serial communication. It allows users to configure various temperature settings and monitor real-time thermistor data, including a live graph of temperature variations.


## Table of Contents
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Usage](#usage)
  - [Creating an Executable](#creating-an-executable)

## Features

- **Heater Activation Temperature**: Set the temperature at which the heater will activate.
- **Solenoid Cutoff Temperature**: Set the temperature at which the solenoid will cut off.
- **Cooling Settings**: Enable or disable cooling settings.
- **Live Thermistor Data**: View real-time data from thermistors.
- **Real-Time Graph**: Monitor temperature variations over time on a live graph.

## Installation

### Prerequisites

- Python 3.x
- Optionally, a virtual environment

### Steps

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
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
    - Ensure that you establish a connection to the relevant serial ports. This might involve connecting any hardware components to your computer or configuring virtual serial ports if applicable.

3. **Live Data Graph**:
    - The data is plotted from the time the serial port is connected. You can show or hide the thermistor lines in the graph as needed.

By following these steps, you can effectively utilize the Data Logger app to configure and monitor your temperature settings.

## Creating an Executable

To create an executable file that will run on Windows, use PyInstaller:

```bash
pyinstaller --onefile --add-data "refresh_icon.png:." src\main.py
```

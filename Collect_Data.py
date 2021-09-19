import pandas as pd
import serial
import time
import threading
from matplotlib import pyplot as plt

file_name = "Photodiode_20Hz.csv"

# This code is for listing available serial/COM ports
# from serial.tools import list_ports
# ports = list(list_ports.comports(include_links=False))
# for port in ports:
#     print(port.name)

# Create instance of the Serial class
baud = 115200
arduino = serial.Serial('COM3', baudrate=baud)

# Initialize global variables
run = True
raw_data = []
time_list = []


def collect_data():
    """
    The collect_data function reads serial data and writes to the global raw_data list.  It also
    uses the time.perf_counter to update the time_list allowing for the evaluation of time between samples
    and overall duration.
    """
    global run
    global raw_data
    global time_list

    while run == 1:
        raw_data.append(arduino.readline())
        time_list.append(time.perf_counter())

        # Evaluates global run variable
        if not run:
            arduino.close()
            print('The data collection loop has exited')


def get_input():
    """
    the get_input function is used to signal the collect data thread stop collecting data.
    """
    global run
    print('Press Enter to end data collection')
    input()
    # thread doesn't continue until Enter is pressed
    run = False
    print('run is now:', run)


def convert_to_int(string_data):
    try:
        # Data sent from Arduino is 8-bit Hex
        integer = int(string_data.strip(), 16)
    except ValueError:
        # If unable to convert string of hex bytes to 8-bit integer, write None
        print(string_data)
        integer = None
    return integer


collect = threading.Thread(target=collect_data)
input = threading.Thread(target=get_input)
collect.start()
input.start()
collect.join()

# Convert list to dataframe
df = pd.DataFrame(raw_data, columns=['Raw'])
df['Time'] = time_list

# Filter out first 100 data points, typically odd data and time gaps are within the first 100 readings
df = df[100:]

# Convert raw data from string of hex bytes to 8-bit integer
df['Amplitude'] = df['Raw'].apply(lambda x: convert_to_int(x))

# Write data to CSV file
df.to_csv(file_name, columns=['Raw', 'Time', 'Amplitude'], index=False)
print(f'Data written to {file_name}')

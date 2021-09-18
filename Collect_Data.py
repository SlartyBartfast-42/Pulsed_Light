import pandas as pd
import serial
import threading
import datetime
from matplotlib import pyplot as plt

# from serial.tools import list_ports
# ports = list(list_ports.comports(include_links=False))
# for port in ports:
#     print(port.name)

baud = 115200
run = 1
fileName = "analog_data_2.csv"
arduino = serial.Serial('COM3', baudrate=baud)
raw_data = []
time_list = []
start = datetime.datetime.now()
stop = datetime.datetime.now()


def normal():
    global run
    global raw_data
    global time_list
    global start
    global stop
    # Write column headers
    # with open(fileName, "a") as file:
    #     c1 = 'Amplitude'
    #     c2 = 'Time'
    #     file.write(f'{c1},{c2}\n')  # write data with a newline

    start = datetime.datetime.now()
    while run == 1:
        raw_data.append(arduino.readline())
        time_list.append(datetime.datetime.now())
        # get_data = arduino.readline()
        # data = int(get_data.strip())
        # print(int(get_data.strip()))

        # append the data to the file
        # with open(fileName, "a") as d_file:
        #     # write data with a newline
        #     d_file.write(f'{data},{datetime.datetime.now()}\n')

        if not run:
            stop = datetime.datetime.now()
            print('The while loop is now closing')


def get_input():
    global run
    keystrk = input()
    # thread doesn't continue until key is pressed
    print('You pressed: ', keystrk)
    run = False
    print('run is now:', run)


n = threading.Thread(target=normal)
i = threading.Thread(target=get_input)
n.start()
i.start()
n.join()
i.join()

df = pd.DataFrame(raw_data, columns=['Raw'])
df['Time'] = time_list
df = df[10:-10]
df['Amplitude'] = df['Raw'].apply(lambda x: int(x.strip()))
df.to_csv(fileName, columns=['Amplitude', 'Time'])

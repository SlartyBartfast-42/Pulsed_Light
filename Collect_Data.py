import serial
import threading
import datetime

# from serial.tools import list_ports
# ports = list(list_ports.comports(include_links=False))
# for port in ports:
#     print(port.name)

baud = 9600
run = 1
fileName = "analog_data.csv"
arduino = serial.Serial('COM3', baudrate=baud)



def normal():
    global run
    # Write column headers
    with open(fileName, "a") as file:
        c1 = 'Amplitude'
        c2 = 'Time'
        file.write(f'{c1},{c2}\n')  # write data with a newline
    while run == 1:
        get_data = arduino.readline()
        data = int(get_data.strip())
        # print(int(get_data.strip()))

        # append the data to the file
        with open(fileName, "a") as d_file:
            # write data with a newline
            d_file.write(f'{data},{datetime.datetime.now()}\n')

        if not run:
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

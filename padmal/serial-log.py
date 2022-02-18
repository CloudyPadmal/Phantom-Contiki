import os

import serial as s
import sys
import signal

if len(sys.argv) is not 3:
    print("Port and Log missing")
    exit()

ser = None
try:
    ser = s.Serial(sys.argv[2], baudrate=115200)
except s.SerialException as e:
    print("\033[91mOperation failed for\033[1m", (sys.argv[1]).split("/")[2], "\033[0m")
    exit()
file = open(sys.argv[2], 'w')


def handler(signum, frame):
    ser.close()
    file.close()
    print(os.getpid(), "stopped and cleaned!")
    exit()


signal.signal(signal.SIGABRT, handler)
ser.write(b'\n')
count = 0

while True:
    try:
        line = ser.readline()
        if line:
            L = line.decode('utf-8', errors='ignore')
            file.write(L)
    except Exception as e:
        print("Error: {0}".format(e))
        ser = s.Serial(sys.argv[1], baudrate=115200)
        if count == 1:
            file.close()
            ser.close()
            exit()
        else:
            count = count + 1

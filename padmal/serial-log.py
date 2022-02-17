import os

import serial as s
import sys
import signal

ser = s.Serial(sys.argv[2], baudrate=115200)
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

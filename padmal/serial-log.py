import serial as s
import sys

ser = s.Serial(sys.argv[2], baudrate=115200)
file = open(sys.argv[2], 'w')

ser.write(b'\n')

count = 0

while True:
    try:
        line = ser.readline()
        if line:
            try:
                L = line.decode('utf-8')
                file.write(L)
            except:
                print('Decode: ', line)
                continue
    except Exception as e:
        print("Error: {0}".format(e))
        ser = s.Serial(sys.argv[1], baudrate=115200)
        if count == 1:
            file.close()
            ser.close()
            exit()
        else:
            count = count + 1

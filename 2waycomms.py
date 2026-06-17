import serial
import time

ser = serial.Serial('COM9', 9600, timeout=1)
time.sleep(2)
ini=ser.readline()
print(ini)
while True:
    cmd = input("1: ON   2: OFF      q: QUIT ")

    if cmd == 'q':
        break

    ser.write(cmd.encode())

    time.sleep(0.1)

    if ser.in_waiting:
        print("Arduino:", ser.readline().decode().strip())

ser.close()
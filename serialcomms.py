import serial
import time

ser = serial.Serial('COM7', 9600)
time.sleep(2)

print("Reading data from Arduino B...")

while True:
    if ser.in_waiting > 0:
        cmd = ser.readline().decode().strip()
        print("Received:", cmd)

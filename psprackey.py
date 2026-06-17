import serial
import time

ser = serial.Serial('COM5', 9600) 
time.sleep(2)  

while True:
    num = input("Enter a digit: ")
    ser.write((num + "\n").encode())     
    print("Sent:", num)

import serial
import time

ser = serial.Serial('COM8', 9600)
time.sleep(2)  # wait for Arduino reset

def send_command(cmd):
    ser.write((cmd + "\n").encode())   # Send command with newline
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    return response

print("Type: ON, OFF, STATUS, EXIT")

while True:
    com = input("").strip().upper()

    if com == "1":
        print(send_command("ON"))

    elif com == "2":
        print(send_command("OFF"))

    

    elif com == "q":
        print("Exiting...")
        break

    else:
        print("Unknown command. Use ON / OFF / STATUS / EXIT")

ser.close()



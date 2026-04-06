import serial
import time
import cv2

ser = serial.Serial('COM3', 115200)
time.sleep(2)

print("Reading data ...")

while True:
    
    if ser.in_waiting > 0:
        cmd = ser.readline().decode().strip()
        
    
        if cmd=='ready':
        
            cv2.destroyAllWindows() 
            tag=cv2.imread('atag0.png')
            cv2.imshow('TAG 0 :',tag)
    
        
        if cmd=='next':
        
            cv2.destroyAllWindows() 
            tag=cv2.imread('atag1.png')
            cv2.imshow('TAG 1 :',tag)
        
        if cmd=='prev':
        
            cv2.destroyAllWindows() 
            tag=cv2.imread('atag2.png')
            cv2.imshow('TAG 2 :',tag)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cv2.destroyAllWindows()

# import serial
# import time
# ser=serial.Serial('COM3',115200)
# while True:
#     if ser.in_waiting>0:
#         cmd=ser.readine().decode().strip()
#         print("received",cmd)

# import cv2
# tag=cv2.imread('atag0.png')
# cv2.imshow('frame',tag)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
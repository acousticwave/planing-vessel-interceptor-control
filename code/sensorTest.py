""" Python Modules """
import serial
import time
""" pyBBIO """
import Adafruit_BBIO.UART as UART
""" Developed Module """
import sensor
""" Use UART1 """
UART.setup("UART1")
""" Set Port and Baud-rate"""
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 115200)
ser.close() # Close the UART1 if it is opened
ser.open()
if ser.isOpen():
    while(True):
        print(sensor.EBIIMURead(ser))   # Print roll,pitch and yaw
ser.close()

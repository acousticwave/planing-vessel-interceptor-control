""" Public python modules """
import time
import math
""" BBIO """
import Adafruit_BBIO.ADC as ADC
""" Developed Module """
import control

ADC.setup() #Setup ADC
while(True):
    value1 = ADC.read("AIN1")   #Read ADC value of ADC Ch1
    value2 = ADC.read("AIN2")   #Read ADC value of ADC Ch2
    print(value1, value2)       #Display

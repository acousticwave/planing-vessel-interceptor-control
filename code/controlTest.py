""" Public python modules """
import serial
import numpy as np
import time
""" pyBBIO """
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.PWM as PWM
""" Developed Modules (placed in the same dir.)"""
import sensor
import control
""" Instances """
timeSTMP0 = control.Control()
timeSTMP1 = control.Control()
ctrlRoll = control.Control()
""" Overlay DTO using pyBBIO """
UART.setup("UART1")             # IMU
""" Set port and baud rate """
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 115200)
ser.close()
ser.open()
if ser.isOpen():
    """ Set gain of a PID controllers """
    KD = 0.03
    ctrlRoll.ctrlGain(0,0,KD)   # pidGain(KP, KI, KD)
    """ Error matrices initialization """
    rollEr = np.matrix('0.0 0.0;1 1')       #[t0 e0; t1 e1]
    """ initial time stamp """
    timeSTMP0.timeSTMP()
    """ Open .dat file to record values """
    f = open('controlTest.dat','w')
    f.write(str('t') + '\t' + str('rollEr') + '\t' + str('q') + '\t' + str('u') + '\n')    #Indices
    """ The Main Loop """
    while(True):
        """ Measure current CPU time and update 't' """
        timeSTMP1.timeSTMP()    # Current CPU time
        t = timeSTMP1.STMP - timeSTMP0.STMP # Current CPU time - Initial time stamp
        """ Measure Euler angles """
        EulerAng = sensor.EBIIMURead(ser)
        """ Update the error matrix (2 x 2) """
        rollEr[0] = rollEr[1]
        rollEr[1] = [t, EulerAng[0]]
        """ Derivative control """
        ctrlRoll.dCtrl(rollEr[0,0],rollEr[1,0],rollEr[0,1],rollEr[1,1])
        """ time derivative of roll """
        q = ctrlRoll.ud / KD
        """ Set Motor Positions (refer the calibration chart)"""
        u =  ctrlRoll.ud
        """ record values """
        f.write(str(t) + '\t' + str(EulerAng[0]) + '\t' + str(q) + '\t' + str(u) + '\n')        

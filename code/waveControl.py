""" Public python modules """
import serial
import numpy as np
import time
""" pyBBIO """
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
""" Developed Modules (placed in the same dir.)"""
import sensor
import control
""" Instances """
timeSTMP0 = control.Control()
timeSTMP1 = control.Control()
ctrlRoll = control.Control()
ctrlPitch = control.Control()
""" Overlay DTO using pyBBIO """
PWM.start("P9_14", 10.9, 50, 0)    # PWM.start(pin, duty, freq, polarity)
PWM.start("P9_16", 9.4, 50, 0)    # PWM.start(pin, duty, freq, polarity)
UART.setup("UART1")             # IMU
ADC.setup()                     # ADC
""" Set port and baud rate """
ser = serial.Serial(port = "/dev/ttyO1", baudrate = 115200)
ser.close()
ser.open()
if ser.isOpen():
    """ Position initialization """
    time.sleep(0.5)
    mot1_pos = 10.9 # PWM_mot1 with interceptor Stroke 0% 
    mot2_pos  = 9.4 # PWM_mot2 with interceptor Stroke 0% 
    PWM.set_duty_cycle("P9_14", mot1_pos)
    PWM.set_duty_cycle("P9_16", mot2_pos)
    time.sleep(0.5)
    """ Position initialization for the theoretical 40% stroke"""
    mot1_pos = 9.128 # PWM_mot1 with interceptor Stroke 40% (ideal value) 
    mot2_pos  = 7.628 # PWM_mot2 with interceptor Stroke 40% (ideal value) 
    PWM.set_duty_cycle("P9_14", mot1_pos)
    PWM.set_duty_cycle("P9_16", mot2_pos)
    time.sleep(0.5)
    """ Set gain of a PID controllers """
    KD = 0.02923
    ctrlRoll.ctrlGain(0,0,KD)   # pidGain(KP, KI, KD)
    ctrlPitch.ctrlGain(0,0,KD)  # pidGain(KP, KI, KD)
    """ Error matrices initialization """
    rollEr = np.matrix('0.0 0.0;1 1')       #[t0 e0; t1 e1]
    pitchEr = np.matrix('0.0 0.0;1 1')    #[t0 e0; t1 e1]
    """ initial time stamp """
    timeSTMP0.timeSTMP()
    """ Open .dat file to record values """
    f = open('waveTest.dat','w')
    f.write(str('t') + '\t' + str('rollEr') + '\t' + str('pitchEr') + '\t' + str('ADC_Ch1') + '\t' + str('ADC_Ch2') + '\t' + str('pitchPOT') + '\t' + str('heavePOT') + '\t' + str('q') + '\t' + str('mot1_pos') + '\t' + str('mot2_pos') + '\n')    #Indices
    """ The Main Loop """
    while(True):
        """ Measure current CPU time and update 't' """
        timeSTMP1.timeSTMP()    # Current CPU time
        t = timeSTMP1.STMP - timeSTMP0.STMP # Current CPU time - Initial time stamp
        """ Measure Euler angles """
        EulerAng = sensor.EBIIMURead(ser)
        """ Read ADC values from the potentiometers """
        ADC_Ch1 = ADC.read("AIN1")  # [ADC Value]
        ADC_Ch2 = ADC.read("AIN2")  # [ADC Value]
        """ convert ADC value into physical size """
        pitchPOT = -307 * ADC_Ch1 + 142.2        # [deg]
        heavePOT = -720.53 * ADC_Ch2 + 969.47   # [mm]
        """ Update the error matrices (2 x 2) """
        rollEr[0] = rollEr[1]
        rollEr[1] = [t, EulerAng[0]]
        pitchEr[0] = pitchEr[1]
        pitchEr[1] = [t, EulerAng[1]]
        """ Derivative control """
        ctrlRoll.dCtrl(rollEr[0,0],rollEr[1,0],rollEr[0,1],rollEr[1,1])
        ctrlPitch.dCtrl(pitchEr[0,0],pitchEr[1,0],pitchEr[0,1],pitchEr[1,1])
        """ time derivative of pitch """
        q = ctrlPitch.ud / KD
        """ Set Motor Positions (refer the calibration chart)"""
        mot1_pos = 9.128 - ctrlPitch.ud
        mot2_pos  = 7.628 - ctrlPitch.ud
        PWM.set_duty_cycle("P9_14", mot1_pos)
        PWM.set_duty_cycle("P9_16", mot2_pos)
        """ record values """
        f.write(str(t) + '\t' + str(EulerAng[0]) + '\t' + str(EulerAng[1]) + '\t' + str(ADC_Ch1) + '\t' + str(ADC_Ch2) + '\t' + str(pitchPOT) + '\t' + str(heavePOT) + '\t' + str(q) + '\t' + str(mot1_pos) + '\t' + str(mot2_pos) + '\n')        
ser.close()

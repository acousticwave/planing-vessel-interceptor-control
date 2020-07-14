""" Public Python Modules"""
import time
import math
""" BBIO """
import Adafruit_BBIO.PWM as PWM
""" Developed Modules """
import control
""" Instances """
timeSTMP0 = control.Control()
timeSTMP1 = control.Control()
""" Start and set duty as '0' """
PWM.start("P9_14", 10.9, 50, 0) # PWM.start(pin, duty, freq, polarity)
PWM.start("P9_16", 9.4, 50, 0)  # PWM.start(pin, duty, freq, polarity)
""" initial time (t_0)"""
timeSTMP0.timeSTMP()    # t_0
""" Sinusoidal Motion"""
while(True):
 timeSTMP1.timeSTMP()   # Current CPU time (t_c)
 t = timeSTMP1.STMP - timeSTMP0.STMP # t = t_c - t_0
 ome = 1            # Period setting
 mot_pos1 = 2.0*math.sin(ome*t) + 8.6    # Motor Position Update (Mot1)
 mot_pos2 = 2.0*math.sin(ome*t) + 7.2    # Motor Position Update (Mot2)
 PWM.set_duty_cycle("P9_14",mot_pos1)    # Set Motor Position (Mot1)
 PWM.set_duty_cycle("P9_16",mot_pos2)    # Set Motor Position (Mot2)
PWM.stop("P9_14")
PWM.stop("P9_16")
PWM.cleanup()


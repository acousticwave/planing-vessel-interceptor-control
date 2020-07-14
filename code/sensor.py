""" 
Data from the EBIIMU_V3:
  *roll,pitch,yaw\r\n (in string format)
  EBIIMURead(ser) parses the data and returns (roll, pitch, yaw)
Usage:  
  - Put an instance into 'ser' e.g. EulerAng = sensor.EBIIMURead(ser),
  then we can extract a roll using the following command
  roll = EulerAng[0]
  - We can extract a pitch using the following command
  pitch = EulerAng[1]
  - We can extract a yaw using the following command
  yaw = EulerAng[2]
"""
def EBIIMURead(ser):
    buf0 = str()    # An empty string buffer
    flag = True     # A flag informs whether '\r\n' is included in buf0 
    while(flag):    # repeat until '\r\n' is detected in buf0
        buf1 = ser.read(1)
        buf0 = buf0 + buf1
        if ('\r\n' in buf0):
            flag = False
    idxSP1 = buf0.find(',') # index of the first comma in buf0 
    idxSP2 = buf0.find(',', idxSP1 + 1) # index of the second comma in buf0
    roll = float(buf0[buf0.find('*') + 1 : idxSP1]) # Coordinate def. of the KRISO ASV
    pitch  = - float(buf0[idxSP1 + 1 : idxSP2]) # Coordinate def. of the KRISO ASV
    yaw = float(buf0[idxSP2 + 1 : buf0.find('\r\n')]) # Not considered     
    return roll, pitch, yaw
"""
#def LordSens_3DM_GX4_25 (ser): # to be updated
"""

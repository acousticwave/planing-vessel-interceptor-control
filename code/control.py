""" Public Python module """
import time
class Control:
    """ return CPU time"""
    def timeSTMP(self):
        #self.STMP =  int(round(1000 * time.time()))    # [ms] setting
        self.STMP =  time.time()                        # [s] setting
    """ We need to set Gains first before using the dctrl"""
    def ctrlGain(self, KP, KI, KD):
        self.KP = float(KP)
        self.KI = float(KI)
        self.KD = float(KD)
    """ Dertivative Controller """
    def dCtrl(self, t0, t1, e0, e1):
        self.ud = self.KD * (e1 - e0) / float(t1 - t0)
    """ Proportional Integral Derivative Controller (To be updated)
    def pidCtrl(self, t0, t1, t2, e0, e1, e2):
        dt0 = t1 - t0
        dt1 = t2 - t1
        self.u = e0/dt0 * self.KD + e1 * (1 - self.KP - self.KD/dt0 + 0.5 * self.KI * dt1 - self.KD/dt0) + e2 * (self.KP + 0.5 * self.KI * dt0 + self.KD/dt1)
    """

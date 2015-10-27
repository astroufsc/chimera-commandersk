# This is an example of an simple instrument.

from chimera.core.chimeraobject import ChimeraObject
from chimera.util.enum import Enum

from skdrv.skdrv import SKDrv

FanDirection = Enum("FORWARD", "REVERSE")


class CSKFan(ChimeraObject):
    __config__ = {'sk_host': '127.0.0.1',
                  'min_speed': 0,
                  'max_speed': 600,
                  'acc_rate': 50,
                  'dec_rate': 100,
                  'motor_rated_speed': 1800,
                  'motor_rated_voltage': 230,
                  'motor_power_factor': 85,
                  'ramp_mode': 1,
                  'dynamicVtoF': 1,
                  'voltage_mode_select': 2,
                  'low_freq_voltage_boost': 10}

    def __init__(self):
        ChimeraObject.__init__(self)

        self.direction = FanDirection.FORWARD

        self.sk = SKDrv()

    def __start__(self):

        self.log.debug('Configuring fan...')
        for par in self.sk.getConfigPars():
            try:
                self.sk[par] = self[par]
            except Exception, e:
                self.log.warning("Could not update controller parameter: %s"%(par))
                self.log.exception(e)

        self.log.debug('Connecting to Commander SK @ %s...'%self["sk_host"])
        self.sk.host = self["sk_host"]
        self.sk.connect()
        self.sk.check_basic()
        self.sk.setup()

        return True

    def getRotation(self):
        return self.sk.check_rotation()

    def setRotation(self,freq):
        """
        Set the rotation frequency in Hz.

        @param freq: Frequency in Hz
        @type  freq: float
        """
        self.sk.write_parm('01.21',int(freq))

    def getDirection(self):
        return self.direction

    def setDirection(self,direction):
        if direction in FanDirection:
            self.direction = direction
        else:
            self.log.warning("Value %s not a valid fan direction. Should be one of %s. Leaving unchanged."%(direction,
                                                                                    ['%s'%d for d in FanDirection]))

    def startFan(self):
        if self.direction == FanDirection.FORWARD:
            return self.sk.forward()
        elif self.direction == FanDirection.REVERSE:
            return self.sk.reverse()
        else:
            raise IOError("Unrecognized fan direction (%s)."%self.direction)

    def stopFan(self):
        return self.sk.stop()


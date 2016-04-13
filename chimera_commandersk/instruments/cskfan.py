# This is an example of an simple instrument.

from chimera.instruments.fan import FanBase
from chimera.interfaces.fan import FanControllabeSpeed, FanControllabeDirection, FanDirection
from skdrv.skdrv import SKDrv


class CSKFan(FanBase, FanControllabeSpeed, FanControllabeDirection):
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

        FanBase.__init__(self)

        self.direction = FanDirection.FORWARD

        self.sk = SKDrv()

    def __start__(self):

        self.log.debug('Configuring fan...')

        self.sk.min_speed = self['min_speed']
        self.sk.max_speed = self['min_speed']
        self.sk.acc_rate = self['min_speed']
        self.sk.dec_rate = self['min_speed']
        self.sk.motor_rated_speed = self['min_speed']
        self.sk.motor_rated_voltage = self['motor_rated_voltage']
        self.sk.motor_power_factor = self['motor_power_factor']
        self.sk.ramp_mode = self['ramp_mode']
        self.sk.dynamicVtoF = self['dynamicVtoF']
        self.sk.voltage_mode_select = self['voltage_mode_select']
        self.sk.low_freq_voltage_boost = self['low_freq_voltage_boost']

        self.log.debug('Connecting to Commander SK @ %s...' % self["sk_host"])
        self.sk.host = self["sk_host"]
        self.sk.connect()
        self.sk.check_basic()
        self.sk.setup()

        return True

    def getRotation(self):
        return self.sk.check_rotation()

    def setRotation(self, freq):
        """
        Set the rotation frequency in Hz.

        @param freq: Frequency in Hz
        @type  freq: float
        """
        self.sk.write_parm('01.21', int(freq))

    def getDirection(self):
        return self.direction

    def setDirection(self, direction):
        if direction in FanDirection:
            self.direction = direction
        else:
            self.log.warning("Value %s not a valid fan direction. Should be one of %s. Leaving unchanged." % (direction,
                                                                                                              ['%s' % d
                                                                                                               for d in
                                                                                                               FanDirection]))

    def switchOn(self):
        if self.direction == FanDirection.FORWARD:
            return self.sk.forward()
        elif self.direction == FanDirection.REVERSE:
            return self.sk.reverse()
        else:
            raise IOError("Unrecognized fan direction (%s)." % self.direction)

    def switchOff(self):
        return self.sk.stop()

    # TODO: def isFanRunning(self):
    #
    # TODO: def status(self):

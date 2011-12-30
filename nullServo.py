# Some usefull functions:
def ms2float(ms):
    """Convert from ssc32 millisecond notation to an float (-1 to +1)"""
    if not 500 <= ms <= 2500 or not isinstance(ms, int):
        raise ValueError, 'ms must be integer between 500 and 2500'
    f = 2*((float(ms) - 500)/2000) - 1
    return f


def float2ms(f):
    """Convert from an float (-1 to +1) to ssc32 millisecond notation"""
    if not -1 <= f <= 1:
        raise ValueError, 'f must be float between -1 and +1'
    ms = ((float(f) + 1)/2)*2000 + 500
    return int(ms)



class nullServo(object):
    """Class to immitate a servo controller for use with robotArm class.
    All servo values should be given and will return as floats between
    -1 and 1 (representing 0 degrees and 180 degrees, respectively)."""

    NUM_CHANNELS = 32

    def __init__(self, print_commands=False):
        self.last_known = dict()
        self.trims = dict()
        self.print_commands = print_commands

    def write(self, cmd):
        if self.print_commands:
            print cmd

    def servo(self, channel, val, speed=0):
        """Set servo channel to val(-1.0 to +1.0)"""
        cmd = '#' + str(channel) + ' P' \
              + str(float2ms(val + self.trims.get(channel,0.0)))
        if speed:
            cmd += 'S' + str(int(speed))
        self.write(cmd + '  ')
        self.last_known[channel] = val

    def servos(self, channel_dict, time=0):
        """Set multiple servos to values in a dict(ch: val)"""
        cmd = ''
        for ch, val in channel_dict.items():
            cmd += '#' + str(ch) + ' P' \
              + str(float2ms(val + self.trims.get(ch,0.0))) + '  '
        if time:
            cmd += 'T' + str(int(time * 1000))
        self.write(cmd)
        self.last_known.update(channel_dict)

    def get_servo(self, channel):
        """Return last value of servo channel"""
        return self.last_known.get(ch)

    def get_servos(self, channels=None):
        """ Get values for a list of servos or return all servo
    positions for channels=None"""
        if isinstance(channels, (list, tuple)):
            return dict([ (k, self.last_known.get(k)) for k in channels ])
        else:
            return dict(self.last_known)

    def center(self, channels=None):
        """Center servos in channels list, or center all if
    channels=None"""
        d = dict()
        if channels is not None:
            d = d.fromkeys(channels, 0.0)
        else:
            d = d.fromkeys(range(self.NUM_CHANNELS), 0.0)
        self.servos(d)

    def trim(self, channel, val):
        """Set the software offset for servo ch to val"""
        self.trims[channel] = val
        






if __name__ == '__main__':
    print "Null Servo Controller module"
    s = nullServo(True)
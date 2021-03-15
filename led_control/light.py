import board
# import logging
import neopixel

from wapi import colors, led_utils as utils

# logging.basicConfig(level=logging.INFO)
# format = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
# LOGGER = logging.getLogger("light.py")
# fh = logging.FileHandler('/home/pi/logs/smarty-lamps.log')
# fh.setFormatter(format)
# LOGGER.addHandler(fh)

# Current list of programs that are dynamic
# TODO: This will eventually be class-based
dynamic_programs = [
    "pulse",
    "console",
    "red alert",
    "yellow flow",
    "sun",
    "rainbow",
    "alarm"
]


class Light:
    def __init__(self):
        self.num = 45
        self.np = neopixel.NeoPixel(board.D18, self.num)
        self._brightness = 1.0
        self._r = 0
        self._g = 0
        self._b = 0
        self._program = None
        self._dynamic = False
        self._on = True

    def set_static(self, color):
        """Set a static color."""
        self._r, self._g, self._b = colors.get_rgb(color)
        self.np.fill((self._r, self._g, self._b))

    @property
    def program(self):
        """Defines the current setting of the lights."""
        return self._program

    @program.setter
    def program(self, new_program):
        self._program = new_program

    @property
    def on(self):
        """Defines the current power state."""
        return self._on

    @on.setter
    def on(self, state):
        if state == "off":
            self._brightness = 0
            self._on = False
        elif state == "on":
            self._brightness = 1
            self._on = True

    @property
    def dynamic(self):
        """ Defines whether current state is dynamic or static."""
        return self._dynamic

    @dynamic.setter
    def dynamic(self, new_setting):
        self._dynamic = new_setting

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, new_bright):

        # only set if value is valid (b/t 0 and 1)
        if 1 >= new_bright >= 0:
            self.np.brightness = new_bright

    def update(self, prog):
        """Public method - set new program."""
        self.program = prog
        # LOGGER.info("Lights object set to %s", self.program)

        if self.program in dynamic_programs:
            self.dynamic = True
        else:
            self.dynamic = False

        # LOGGER.info("Calling utils function.")
        utils.start_program(self.np, self.program)

        # if self.program in dynamic_programs:
        #     self.dynamic = True
        # else:
        #     self.dynamic = False
        #
        # # dict.get(prog)
        #
        # if prog == "pulse":
        #     utils.pulse(self.np)
        # elif prog == "console":
        #     utils.console(self.np)
        # elif prog == "red alert":
        #     utils.red_alert(self.np)
        # elif prog == "yellow flow":
        #     utils.it_was_all_yellow(self.np)
        # elif prog == "sun":
        #     utils.sun(self.np)
        # elif prog == "rainbow":
        #     utils.rainbow(self.np)
        # elif prog == "alarm":
        #     utils.alarm(self.np)
        # elif prog == "light show":
        #     utils.light_show(self.np)
        # else:
        #     utils.set_color(self.np, prog)

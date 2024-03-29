import board
import neopixel

import config
from wapi import colors, led_utils as utils


# get logger
LOGGER = config.logging_config(__name__)

# Current list of programs that are dynamic
# TODO: This will eventually be class-based
dynamic_programs = utils.programs_dict


class Light:
    def __init__(self):
        self.num = 63
        self.np = neopixel.NeoPixel(board.D18, self.num)
        self._brightness = 1.0
        self._r = 0
        self._g = 0
        self._b = 0
        self._program = None
        self._dynamic = False
        self._on = True
        self._loop = True

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
    def loop(self):
        """Defines whether dynamic loop is currently True/False."""
        return self._loop

    @loop.setter
    def loop(self, switch):
        if switch == True or switch == False:
            self._loop = switch

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
        LOGGER.info("Lights object set to %s", self.program)

        if self.program in dynamic_programs.keys():
            self.dynamic = True
        else:
            self.dynamic = False

        # LOGGER.info("Calling utils function.")
        utils.start_program(self, self.np, self.program)

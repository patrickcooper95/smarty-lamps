import board
import neopixel

from wapi import colors, led_utils

# Current list of programs that are dynamic
# TODO: This will eventually be class-based
dynamic_programs = [
    "pulse",
    "console",
    "red alert",
    "yellow flow",
    "sun",
    "rainbow",
    "wake me up"
]

class Light:
    def __init__(self):
        self.num = 60
        self.np = neopixel.NeoPixel(board.D18, self.num)
        self._brightness = 1.0
        self._r = 0
        self._g = 0
        self._b = 0
        self._program = None
        self._dynamic = False

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

        self._brightness = new_bright

        # Set RGB to nearest whole number when multiplied by brightness
        self._r = round(self._r * self._brightness)
        self._g = round(self._g * self._brightness)
        self._b = round(self._b * self._brightness)
        self.np.fill((self._r, self._g, self._b))

    def update(self, new_setting):
        """Public method - set new program."""
        self.program = new_setting

        if self.program in dynamic_programs:
            self.dynamic = True
        else:
            self.dynamic = False




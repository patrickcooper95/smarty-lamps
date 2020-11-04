from wapi import colors, led_utils


class Program:
    def __init__(self, red, green, blue, dynamic):
        self.dynamic = dynamic
        self.r = red
        self.g = green
        self.b = blue
        self.active = False


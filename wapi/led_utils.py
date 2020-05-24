import random
import sqlite3 as sql
import time


import board
import neopixel

import wapi.colors as colors

np = neopixel.NeoPixel(board.D18, 50)

loop = True

programs = ["pulse", "console"]


def set_color(color):
    """Set a static color."""
    red, green, blue = colors.get_rgb(color)
    np.fill((red, green, blue))


def pulse():
    """Create a blue pulsing effect."""
    r = 0
    g = 0
    b = 255
    while loop:
        try:
            for count in range(100):
                if not loop:
                    break

                np.fill((r, g, b))
                time.sleep(0.05)
                r += 1
                g += 1

            for count in range(100):
                if not loop:
                    break

                r -= 1
                g -= 1
                np.fill((r, g, b))
                time.sleep(0.05)
            # Make blue stay longer
            time.sleep(0.1)

        except KeyboardInterrupt as e:
            raise (e)


def console():
    """Create a starship blinking console effect."""
    orange = (255, 165, 0)
    np.fill(orange)

    while loop:
        try:
            pixel = random.randint(0, 29)
            sleep = random.randint(1, 3)
            np[pixel] = (0, 0, 0)
            np.show()
            time.sleep(sleep)
            np[pixel] = orange
            np.show()
        except KeyboardInterrupt as e:
            raise (e)


def red_alert():
    """Red alert flash."""
    r = 255
    g = 0
    b = 0

    while loop:
        try:
            for count in range(230):
                if not loop:
                    break

                np.fill((r, g, b))
                r -= 1

            for count in range(230):
                if not loop:
                    break

                np.fill((r, g, b))
                r += 1
            time.sleep(1.0)

        except KeyboardInterrupt as e:
            raise (e)



# def set_brightness(level):
#     if level <= 1 and level >= 0:
#         brightness = level
#         r = int(r * level)
#         self.g = int(self.g * level)
#         self.b = int(self.b * level)
#         self.update_program()
#     else:
#         print("Invalid brightness level.")

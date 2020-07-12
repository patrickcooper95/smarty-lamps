import datetime
import random
import sqlite3 as sql
import time


import board
import neopixel

import wapi.colors as colors
import wapi.get_sun as get_sun

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


def it_was_all_yellow():
    """Create lights for Yellow."""
    yellow = (255, 255, 0)
    np.fill(yellow)

    while loop:
        try:
            green = 255
            for inc in range(172):
                if not loop:
                    break

                green -= 1
                for pixel in range(50):
                    np[pixel] = (255, green, 0)
                time.sleep(0.5)

            for inc_up in range(172):
                if not loop:
                    break

                green += 1
                for pixel in range(50):
                    np[pixel] = (255, green, 0)
                time.sleep(0.5)

        except KeyboardInterrupt as e:
            raise (e)


def console():
    """Create a starship blinking console effect."""
    init_color = (255, 100, 0)

    np.fill((0, 0, 0))
    init_num = random.randint(0, 49)
    init_pixels = []
    for p in range(init_num):
        pixel = random.randint(0, 49)
        init_pixels.append(pixel)
        np[pixel] = init_color

    while loop:
        try:
            pixel = random.randint(0, 49)
            index = random.randint(1, 3)
            sleep = [0.5, 1, 1.5]
            np[pixel] = (0, 0, 0)
            np.show()
            time.sleep(sleep[index-1])
            np[pixel] = init_color
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


def rainbow():
    """Rainbow effect."""
    r = 255
    g = 0
    b = 0

    while loop:
        try:
            for count in range(255):
                if not loop:
                    break

                np.fill((r, g, b))
                r -= 1
                g += 1

                time.sleep(1.0)

            for count in range(255):
                if not loop:
                    break

                np.fill((r, g, b))
                g -= 1
                b += 1

                time.sleep(1.0)

            for count in range(255):
                if not loop:
                    break

                np.fill((r, g, b))
                b -= 1
                r += 1

                time.sleep(1.0)

        except KeyboardInterrupt as e:
            raise (e)


def sun():
    """Lighting effects programmed to follow the sunrise and sunset."""
    first_time = True
    TIME = datetime.datetime.strptime("12:05:00", "%H:%M:%S").time()
    daylight = (255, 255, 255)
    night = (0, 8, 16)
    r = 0
    g = 0
    b = 0

    while loop:
        current_time = datetime.datetime.now().time().replace(second=0, microsecond=0)
        if first_time or (current_time == TIME):
            sun = read_sun()

            # These will remain Datetime objects for addition/subtraction operations.
            sunrise = round_times(sun.split(",")[0])
            sunset = round_times(sun.split(",")[1])

            if first_time:
                if (current_time > sunrise.time()) and (current_time < sunset.time()):
                    np.fill(daylight)
                    r = 255
                    g = 255
                    b = 255
                else:
                    np.fill(night)
                    r = 0
                    g = 8
                    b = 16

                first_time = False

        if current_time == (sunrise - datetime.timedelta(minutes=5)).time().replace(second=0, microsecond=0):
            for num in range(239):
                if not loop:
                    break

                # Catch up red and green pixels to blue
                if num < 16:
                    r += 2
                else:
                    r += 1

                if num < 8:
                    g += 2
                else:
                    g += 1

                b += 1

                np.fill((r, g, b))
                time.sleep(3.0)

        if current_time == (sunset - datetime.timedelta(minutes=5)).time().replace(second=0, microsecond=0):
            for num in range(239):
                if not loop:
                    break

                # Catch up red and green pixels to blue
                if num < 16:
                    r -= 2
                else:
                    r -= 1

                if num < 8:
                    g -= 2
                else:
                    g -= 1

                b -= 1

                np.fill((r, g, b))
                time.sleep(3.0)

def read_sun():
    """Read the latest sunrise/sunset times."""
    with open('/home/pi/WAPI/smarty-lamps/wapi/sun.txt', 'r') as file:
        times = file.read()
    file.close()
    return times


def round_times(time):
    """Convert string to datetime and round to nearest minute."""
    time = time.strip()
    new_time = datetime.datetime.strptime(time, "%H:%M:%S")
    return new_time

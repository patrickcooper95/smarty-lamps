import datetime
import os
import random
import sqlite3 as sql
import time

import wapi.colors as colors
import wapi.configs as configs
import wapi.get_sun as get_sun


loop = True


def set_color(np, color):
    """Set a static color."""
    red, green, blue = colors.get_rgb(color)
    np.fill((red, green, blue))


def pulse(np):
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


def it_was_all_yellow(np):
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
                for pixel in range(np.num):
                    np[pixel] = (255, green, 0)
                time.sleep(0.5)

            for inc_up in range(172):
                if not loop:
                    break

                green += 1
                for pixel in range(np.num):
                    np[pixel] = (255, green, 0)
                time.sleep(0.5)

        except KeyboardInterrupt as e:
            raise (e)


def console(np):
    """Create a starship blinking console effect."""
    init_color = (255, 100, 0)

    np.fill((0, 0, 0))
    init_num = random.randint(0, np.num)
    init_pixels = []
    for p in range(init_num):
        pixel = random.randint(0, np.num)
        init_pixels.append(pixel)
        np[pixel] = init_color

    while loop:
        try:
            pixel = random.randint(0, np.num)
            index = random.randint(1, 3)
            sleep = [0.5, 1, 1.5]
            np[pixel] = (0, 0, 0)
            np.show()
            time.sleep(sleep[index-1])
            np[pixel] = init_color
            np.show()
        except KeyboardInterrupt as e:
            raise (e)


def red_alert(np):
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


def rainbow(np):
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

            
def light_show(np):
    """Light show effect."""
    r = 255
    g = 255
    b = 255

    np.fill((r, g, b))

    for led in range(1, np.num, 2):
        np[led] = (255, 0, 0)

    while loop:
        for led in range(1, np.num, 2):
            np[led] = (255, 255, 255)
        time.sleep(0.3)
        for led in range(1, np.num, 2):
            np[led] = (255, 0, 0)


def sun(np):
    """Lighting effects programmed to follow the sunrise and sunset."""
    first_time = True
    TIME = datetime.datetime.strptime("12:05:00", "%H:%M:%S").time()
    check_times = False
    daylight = (255, 255, 255)
    night = (1, 1, 1)
    r = 0
    g = 0
    b = 0

    while loop:
        current_time = datetime.datetime.now().time().replace(second=0, microsecond=0)

        if first_time or check_times:

            # TODO: Find a way to only check this once when the criteria is met.
            sun = read_sun()

            # These will remain Datetime objects for addition/subtraction operations.
            sunrise = round_times(sun.split(",")[0])
            sunset = round_times(sun.split(",")[1])

            check_times = False

            if first_time:
                if (current_time > sunrise.time()) and (current_time < sunset.time()):
                    np.fill(daylight)
                    r = 255
                    g = 255
                    b = 255
                else:
                    np.fill(night)
                    r = 1
                    g = 1
                    b = 1

                first_time = False


        times = (sunrise.hour, sunset.hour, TIME.hour)

        if current_time.hour in times:

            if current_time == TIME:
                check_times = True

            if current_time == (sunrise - datetime.timedelta(minutes=5)).time().replace(second=0, microsecond=0):
                for num in range(255):
                    if not loop:
                        break

                    # Slowly increase brightness
                    r += 1
                    g += 1
                    b += 1

                    np.fill((r, g, b))
                    time.sleep(3.0)

            if current_time == (sunset - datetime.timedelta(minutes=5)).time().replace(second=0, microsecond=0):
                for num in range(255):
                    if not loop:
                        break

                    # Slowly decrease brightness
                    r -= 1
                    g -= 1
                    b -= 1

                    np.fill((r, g, b))
                    time.sleep(3.0)
        time.sleep(1.0)


def alarm(np):
    """Simulate sunlight through the window at specified time."""
    r, g, b = 0, 0, 0
    np.fill((r, g, b))

    conn = sql.connect(configs.db_path)
    cur = conn.cursor()
    result = cur.execute('SELECT * FROM times WHERE id="alarm"').fetchall()
    alarm_time = result[0][1]
    conn.close()

    wake_up_time = datetime.datetime.strptime(alarm_time, "%H:%M:%S").time()

    while loop:
        current_time = datetime.datetime.now().time().replace(second=0, microsecond=0)
        if wake_up_time.hour == current_time.hour:
            if wake_up_time == current_time:
                np.fill((255, 128, 0))
                break
        time.sleep(1.0)


def read_sun():
    """Read the latest sunrise/sunset times."""
    with open(os.path.join(configs.base_path, "wapi", "sun.txt"), "r") as file:
        times = file.read()
    file.close()
    return times


def round_times(time):
    """Convert string to datetime and round to nearest minute."""
    time = time.strip()
    new_time = datetime.datetime.strptime(time, "%H:%M:%S")
    return new_time


def rest(rise_time, set_time):
    """Get the current time and compare to key sun times."""
    right_now = datetime.datetime.now().replace(second=0, microsecond=0)
    check_time = datetime.datetime.strptime("12:05:00", "%H:%M:%S")
    sunrise = rise_time
    sunset = set_time

    # Get time deltas
    time_to_sunrise = (sunrise - right_now)
    time_to_sunset = (sunset - right_now)

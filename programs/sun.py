import datetime
import os
import time

from wapi import configs


def sun(light_obj, np):
    """Lighting effects programmed to follow the sunrise and sunset."""
    first_time = True
    TIME = datetime.datetime.strptime("12:05:00", "%H:%M:%S").time()
    check_times = False
    daylight = (255, 255, 255)
    night = (1, 1, 1)
    r = 0
    g = 0
    b = 0

    while light_obj.loop:
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
                    if not light_obj.loop:
                        break

                    # Slowly increase brightness
                    r += 1
                    g += 1
                    b += 1

                    np.fill((r, g, b))
                    time.sleep(3.0)

            if current_time == (sunset - datetime.timedelta(minutes=5)).time().replace(second=0, microsecond=0):
                for num in range(255):
                    if not light_obj.loop:
                        break

                    # Slowly decrease brightness
                    r -= 1
                    g -= 1
                    b -= 1

                    np.fill((r, g, b))
                    time.sleep(3.0)
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

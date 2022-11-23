import logging
import time
import threading

from add_ons.nyct import nyct as NYCT
from add_ons.nyct.utils import Config


# 6 train is green - modify if other routes are tracked
SERVICE = "6"
SERVICE_SEGMENT = "M"
SERVICE_COLOR = (0, 255, 0)
STOPPED_DELAY = 1
LOGGER = logging.getLogger()


def trunc_float(num):
    return int(num*100)/100


def service_color_mapping():
    """More advanced color mapping for future use."""
    pass


def train_engine(np, led, fade, event):
    while True:
        if fade:
            r, g, b = 0, 0, 0
            for i in range(200):
                if event.is_set():
                    np[led] = ((0, 0, 0))
                    break
                np[led] = ((r, g, b))
                time.sleep(0.005)
                g += 1
            for i in range(200):
                if event.is_set():
                    np[led] = ((0, 0, 0))
                    break
                np[led] = ((r, g, b))
                time.sleep(0.005)
                g -= 1
        else:
            np[led] = (SERVICE_COLOR)
            time.sleep(STOPPED_DELAY)
            np[led] = ((0, 0, 0))
            time.sleep(STOPPED_DELAY)
        if event.is_set():
            break


def train_tracker(light_obj, np):
    """Display NY Subway activity on lights."""

    # Start empty
    np.fill((0, 0, 0))
    trains = NYCT.get_trains(SERVICE, SERVICE_SEGMENT)

    while light_obj.loop:
        event = threading.Event()
        thread_list = []
        leds_in_use = []

        for train in trains["data"]:
            led = Config["led_station_mapping"][int(SERVICE)][int(train["stop_id"][:-1])]
            if led in leds_in_use:
                continue
            leds_in_use.append(led)

            fade = True if train["status"] in ("IN_TRANSIT_TO", "INCOMING_AT") else False

            new_thread = threading.Thread(target=train_engine, args=(np, led, fade, event))
            thread_list.append(new_thread)
            new_thread.start()

        LOGGER.info(f"{len(trains)} new threads started to display trains")
        time.sleep(10)
        LOGGER.info("Retrieving trains from NYCT...")
        start = time.time()
        trains = NYCT.get_trains(SERVICE, SERVICE_SEGMENT)
        LOGGER.info(f"Trains retrieved in: {trunc_float(time.time()-start)} seconds")
        event.set()
        LOGGER.info(f"Sending stop events to threads: {thread_list}")

        for index, thread in enumerate(thread_list):
            thread.join()

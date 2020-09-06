import daemon
import logging
import threading
import time
import sqlite3 as sql

import wapi.led_utils as utils
from led_control import Light

LOGGER = logging.getLogger()
logging.basicConfig(filename='daemon.log', level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fh = logging.FileHandler("./daemon.log")
LOGGER.addHandler(fh)
logging.info("Daemon starting.")

# Create Light object to be used
lights = Light()


class LedWorker(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(LedWorker, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()
        self._stop_event.is_set()

    def stopped(self):
        return self._stop_event.is_set()


def set_program(prog):
    if prog == "pulse":
        utils.pulse()
    elif prog == "console":
        utils.console()
    elif prog == "red alert":
        utils.red_alert()
    elif prog == "yellow flow":
        utils.it_was_all_yellow()
    elif prog == "sun":
        utils.sun()
    elif prog == "rainbow":
        utils.rainbow()
    elif prog == "wake me up":
        utils.alarm()
    else:
        utils.set_color(prog)


def main_program():
    while True:
        time.sleep(0.05)
        conn = sql.connect('/home/pi/WAPI/smarty-lamps/devices.db')
        cur = conn.cursor()
        new_state = cur.execute('SELECT devices.program FROM devices WHERE identifier="desk-led"').fetchall()[0][0]
        conn.close()
        if not lights.program == new_state:

            logging.info("Change detected. Updating lights to %s.", new_state)

            # Stop current forked thread for the dynamic program
            if lights.dynamic:
                utils.loop = False
                time.sleep(0.1)

                try:
                    led_worker.join()
                except NameError as e:
                    logging.info(e)

            lights.update(new_state)

            led_worker = LedWorker(target=set_program, args=(new_state,))
            utils.loop = True

            logging.info("Starting new thread.")
            led_worker.start()


context = daemon.DaemonContext(
    files_preserve = [fh.stream,]
    )

with context:
    main_program()

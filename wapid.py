import daemon
import logging
import os
import threading
import time
import sqlite3 as sql

import wapi.configs as configs
import wapi.led_utils as utils

from led_control import Light

logging.basicConfig(level=logging.INFO)
format = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
LOGGER = logging.getLogger("wapid.py")
fh = logging.FileHandler('/home/pi/logs/smarty-lamps.log')
fh.setFormatter(format)
LOGGER.addHandler(fh)

# First logging message - show daemon is online
LOGGER.info("Daemon starting...")

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
    lights.update(prog)
    LOGGER.info("Spawned thread finished.")


def main_program():
    while True:
        time.sleep(0.05)
        conn = sql.connect(os.path.join(configs.db_path))
        cur = conn.cursor()
        new_state = cur.execute('SELECT devices.program FROM devices WHERE identifier="desk-led"').fetchall()[0][0]
        conn.close()
        if not lights.program == new_state:

            LOGGER.info("Change detected. Updating lights to %s.", new_state)

            # Stop current forked thread for the dynamic program
            if lights.dynamic:
                lights.loop = False
                time.sleep(0.1)

                try:
                    led_worker.join()
                except NameError as e:
                    LOGGER.info(e)

            # Start new thread to initiate new program
            led_worker = LedWorker(target=set_program, args=(new_state,))
            lights.loop = True

            LOGGER.info("Starting new thread.")
            led_worker.start()

            if lights.dynamic:
                LOGGER.info("Program is dynamic.")
            else:
                LOGGER.info("Program is static.")


context = daemon.DaemonContext(
    files_preserve = [fh.stream,]
    )

with context:
    main_program()

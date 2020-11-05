import daemon
import logging
import os
import threading
import time
import sqlite3 as sql

import wapi.configs as configs
import wapi.led_utils as utils

from led_control import Light

logging.basicConfig(filename='/home/pi/logs/smarty-lamps.log', level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
LOGGER = logging.getLogger("wapid.py")
LOGGER.info("Daemon starting.")

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
                utils.loop = False
                time.sleep(0.1)

                try:
                    led_worker.join()
                except NameError as e:
                    LOGGER.info(e)

            # Update Light object
            # lights.update(new_state)

            # Start new thread to initiate new program
            # TODO: Eventually, change this to only kick off new thread if dynamic
            led_worker = LedWorker(target=set_program, args=(new_state,))
            utils.loop = True

            LOGGER.info("Starting new thread.")
            led_worker.start()

            LOGGER.info(f"Program set to: {lights.program}")
            LOGGER.info(f"Brightness: {lights.brightness}")
            if lights.dynamic:
                LOGGER.info("Program is dynamic.")
            else:
                LOGGER.info("Program is static.")


context = daemon.DaemonContext(
    files_preserve = [fh.stream,]
    )

with context:
    main_program()

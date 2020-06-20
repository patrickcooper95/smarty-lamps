import daemon
import threading
import time
import sqlite3 as sql

import wapi.led_utils as utils


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
    else:
        utils.set_color(prog)


def main_program():
    current_state = ""
    while True:
        time.sleep(0.05)
        conn = sql.connect('/home/pi/WAPI/smarty-lamps/devices.db')
        cur = conn.cursor()
        new_state = cur.execute('SELECT devices.program FROM devices WHERE identifier="desk-led"').fetchall()[0][0]
        # dynamic = cur.execute(f'SELECT * FROM colors WHERE name={new_state}').fetchall()[0][4]
        conn.close()
        if not current_state == new_state:
            utils.loop = False

            led_worker = LedWorker(target=set_program, args=(new_state,))
            utils.loop = True
            led_worker.start()
            current_state = new_state


context = daemon.DaemonContext()

with context:
    main_program()

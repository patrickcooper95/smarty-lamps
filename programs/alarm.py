import datetime
import time
import sqlite3 as sql

from wapi import configs


def alarm(obj, np):
    """Simulate sunlight through the window at specified time."""
    r, g, b = 0, 0, 0
    np.fill((r, g, b))

    conn = sql.connect(configs.db_path)
    cur = conn.cursor()
    result = cur.execute('SELECT * FROM times WHERE id="alarm"').fetchall()
    alarm_time = result[0][1]
    conn.close()

    wake_up_time = datetime.datetime.strptime(alarm_time, "%H:%M:%S").time()

    while obj.loop:
        current_time = datetime.datetime.now().time().replace(second=0, microsecond=0)
        if wake_up_time.hour == current_time.hour:
            if wake_up_time == current_time:
                np.fill((100, 100, 100))
                break
        time.sleep(1.0)

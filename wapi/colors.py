"""Colors that can be used for the LEDs."""
from ast import literal_eval
import os
import sqlite3 as sql

from wapi import configs


def get_rgb(color):
    conn = sql.connect(os.path.join(configs.db_path))
    cur = conn.cursor()
    rgb = cur.execute(f'SELECT colors.r, colors.g, colors.b FROM colors WHERE lower(name)="{color}"').fetchall()[0]
    conn.close()
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    return red, green, blue


    # colors = config['Colors']
    # for key in colors:
    #     if key.lower() == color.lower():
    #         return literal_eval(colors[key])
    #     # TODO Begin the error handling process here if an invalid color is passed
    #     # else:
    #         # return "Not a valid color."

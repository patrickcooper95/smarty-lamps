import random
import time


def christmas_tree(light_obj, np):
    purple = (128, 0, 128)
    orange = (255, 165, 0)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    colors = [
        purple,
        orange,
        yellow,
        green,
        red,
        blue,
    ]

    for led in range(light_obj.num):
        rand = random.randint(0, len(colors) - 1)
        np[led] = colors[rand]

    while light_obj.loop:
        rand_led = random.randint(0, light_obj.num - 1)
        rand_color = random.randint(0, len(colors) - 1)

        np[rand_led] = colors[rand_color]

        time.sleep(0.5)

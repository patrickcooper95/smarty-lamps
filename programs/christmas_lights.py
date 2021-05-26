import random
import time


def christmas_lights(light_obj, np):
    """Christmas lights program."""
    even_leds = []
    odd_leds = []

    for i in range(light_obj.num):
        if i % 2 == 0:
            even_leds.append(i)
        else:
            odd_leds.append(i)

    for even in even_leds:
        np[even] = (255, 0, 0)
    for odd in odd_leds:
        np[odd] = (0, 255, 0)

    while light_obj.loop:
        time.sleep(0.5)

        rand = random.randint(0, light_obj.num - 1)
        rand_color = random.randint(0, 1)

        if rand_color:
            set = (0, 255, 0)
        else:
            set = (255, 0, 0)

        np[rand] = set

        time.sleep(0.5)
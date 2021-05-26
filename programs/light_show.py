import time


def light_show(light_obj, np):
    """Light show effect."""
    r = 255
    g = 255
    b = 255

    np.fill((r, g, b))

    for led in range(1, np.num, 2):
        np[led] = (255, 0, 0)

    while light_obj.loop:
        for led in range(1, np.num, 2):
            np[led] = (255, 255, 255)
        time.sleep(0.3)
        for led in range(1, np.num, 2):
            np[led] = (255, 0, 0)

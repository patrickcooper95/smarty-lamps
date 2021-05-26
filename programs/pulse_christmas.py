import time


def pulse_christmas(light_obj, np):
    """Create a blue pulsing effect."""
    r = 255
    g = 0
    b = 0
    while light_obj.loop:
        for count in range(255):
            if not light_obj.loop:
                break

            np.fill((r, g, b))
            time.sleep(0.05)
            r -= 1
            g += 1

        for count in range(255):
            if not light_obj.loop:
                break

            r += 1
            g -= 1
            np.fill((r, g, b))
            time.sleep(0.05)
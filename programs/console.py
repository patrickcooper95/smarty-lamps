import random
import time


def console(light_obj, np):
    """Create a starship blinking console effect."""
    init_color = (255, 100, 0)

    np.fill(init_color)
    init_num = random.randint(0, light_obj.num)
    init_pixels = []
    for p in range(init_num):
        pixel = random.randint(0, light_obj.num)
        init_pixels.append(pixel)
        np[pixel] = init_color

    while light_obj.loop:
        try:
            pixel = random.randint(0, light_obj.num)
            index = random.randint(1, 3)
            sleep = [0.5, 1, 1.5]
            np[pixel] = (0, 0, 0)
            np.show()
            time.sleep(sleep[index-1])
            np[pixel] = init_color
            np.show()
        except KeyboardInterrupt as e:
            raise (e)

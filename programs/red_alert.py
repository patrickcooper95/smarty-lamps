import time


def red_alert(light_obj, np):
    """Red alert flash."""
    r = 255
    g = 0
    b = 0

    while light_obj.loop:
        try:
            for count in range(230):
                if not light_obj.loop:
                    break

                np.fill((r, g, b))
                r -= 1

            for count in range(230):
                if not light_obj.loop:
                    break

                np.fill((r, g, b))
                r += 1
            time.sleep(1.0)

        except KeyboardInterrupt as e:
            raise (e)

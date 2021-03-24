import time


def rainbow(light_obj, np):
    """Rainbow effect."""
    r = 255
    g = 0
    b = 0

    while light_obj.loop:
        try:
            for count in range(255):
                if not light_obj.loop:
                    break

                np.fill((r, g, b))
                r -= 1
                g += 1

                time.sleep(1.0)

            for count in range(255):
                if not light_obj.loop:
                    break

                np.fill((r, g, b))
                g -= 1
                b += 1

                time.sleep(1.0)

            for count in range(255):
                if not light_obj.loop:
                    break

                np.fill((r, g, b))
                b -= 1
                r += 1

                time.sleep(1.0)

        except KeyboardInterrupt as e:
            raise (e)


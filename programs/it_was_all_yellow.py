import time


def it_was_all_yellow(light_obj, np):
    """Create lights for Yellow."""
    yellow = (255, 255, 0)
    np.fill(yellow)

    while light_obj.loop:
        try:
            green = 255
            for inc in range(172):
                if not light_obj.loop:
                    break

                green -= 1
                np.fill((255, green, 0))
                time.sleep(0.5)

            for inc_up in range(172):
                if not light_obj.loop:
                    break

                green += 1
                np.fill((255, green, 0))
                time.sleep(0.5)

        except KeyboardInterrupt as e:
            raise (e)

import time



loop = True


def pulse(np):
    """Create a blue pulsing effect."""
    r = 0
    g = 0
    b = 255
    while loop:
        try:
            for count in range(100):
                if not loop:
                    break

                np.fill((r, g, b))
                time.sleep(0.05)
                r += 1
                g += 1

            for count in range(100):
                if not loop:
                    break

                r -= 1
                g -= 1
                np.fill((r, g, b))
                time.sleep(0.05)
            # Make blue stay longer
            time.sleep(0.1)

        except KeyboardInterrupt as e:
            raise (e)

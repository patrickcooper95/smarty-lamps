import time



loop = True

def it_was_all_yellow(np):
    """Create lights for Yellow."""
    yellow = (255, 255, 0)
    np.fill(yellow)

    while loop:
        try:
            green = 255
            for inc in range(172):
                if not loop:
                    break

                green -= 1
                np.fill((255, green, 0))
                time.sleep(0.5)

            for inc_up in range(172):
                if not loop:
                    break

                green += 1
                np.fill((255, green, 0))
                time.sleep(0.5)

        except KeyboardInterrupt as e:
            raise (e)

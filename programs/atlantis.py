import time


def atlantis(light_obj, np):
    """Create a pink,blue,teal effect."""
    np.fill((255, 20, 147))
    while light_obj.loop:
        try:
            for count in range(light_obj.num):
                if not light_obj.loop:
                    break

                np[count] = ((0, 128, 128))
                time.sleep(0.1)

#            time.sleep(2.0)

            for count in range(light_obj.num):
                if not light_obj.loop:
                    break

                np[count] = ((0, 0, 255))
                time.sleep(0.1)

#            time.sleep(2.0)

            for count in range(light_obj.num):
                if not light_obj.loop:
                    break

                np[count] = ((255, 20, 147))
                time.sleep(0.1)

#            time.sleep(2.0)

        except KeyboardInterrupt as e:
            raise (e)

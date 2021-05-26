import datetime
from importlib import reload
from inspect import getmembers, isfunction

import config
import wapi.colors as colors

LOGGER = config.logging_config(__name__)

loop = True

import programs


def set_color(np, color):
    """Set a static color."""
    red, green, blue = colors.get_rgb(color)
    np.fill((red, green, blue))


programs_dict = {}


def index():
    """ Reindex the programs package for new programs. """
    LOGGER.info("Attempting to load programs package")

    try:
        reload(programs)
    except Exception as e:
        print(e)
        # LOGGER.error(e)

    functions = getmembers(programs, isfunction)
    LOGGER.info(len(functions))
    for func in functions:
        programs_dict[func[0]] = func[1]

    LOGGER.info("Programs indexed successfully")


def start_program(obj, np, prog):
    """ Set the lights to the new program. """
    if obj.dynamic:
        LOGGER.info("Starting program: %s", prog)
        programs_dict[prog](obj, np)
        LOGGER.info("Program started")
    else:
        # Set static color
        set_color(np, prog)

# Run index every time led_utils is imported
index()


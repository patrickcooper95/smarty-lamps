import logging
import daemon
import daemon.pidfile
import subprocess

from wapi import led_utils as utils, configs

presets = {"pulse": utils.pulse}


def set_program(request):
    for key in presets.keys():
        if key == request:
            logger = logging.getLogger("DaemonLog")
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler('logger.log')
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            logger.addHandler(handler)


    for con in configs.config:
        if con == request:
            utils.set_color(request)

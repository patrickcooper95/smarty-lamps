import logging
import os

import yaml


environment = os.getenv("ENV", "local")

with open("./wapi/config.yaml", 'r') as config_file:
    try:
        base_configs = yaml.safe_load(config_file)
    except yaml.YAMLError as exc:
        print(exc)


def logging_config(name):
    if environment in ("DEV", "PROD"):
        logging.basicConfig(filename=f'{base_configs["CONFIG_LOG_DIR"]}smarty-lamps.log',
                            level=logging.INFO,
                            format='%(asctime)s | %(levelname)s | %(name)s | %(threadName)s | %(message)s')
    else:
        # Don't log to a file if local / unittest
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s | %(levelname)s | %(name)s | %(threadName)s | %(message)s')
    return logging.getLogger(name)

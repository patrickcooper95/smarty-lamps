import logging


def logging_config(name):
    logging.basicConfig(filename='/home/pi/logs/smarty-lamps.log',
                        level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(name)s | %(threadName)s | %(message)s')
    return logging.getLogger(name)

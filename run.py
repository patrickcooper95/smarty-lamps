import argparse

from device_registry import app
from wapi import configs

parser = argparse.ArgumentParser()
parser.add_argument('--environment', help="Specify the environment to run.")
args = parser.parse_args()

# TODO Finish adding environment control - add Configs class in wapi/configs.py
path = args.environment


app.run(host='0.0.0.0')
# app.run(host='0.0.0.0', port=80, debug=True)

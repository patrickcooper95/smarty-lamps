import logging
import os

import yaml

# Get environment variable for environment - default to DEV if not found
# TODO: Use dot-env to make this work
environment = os.getenv("ENV", "DEV")
base_path = os.path.join("/home", "pi", environment, "smarty-lamps")
db_path = os.path.join('/home', 'sqlite', 'live', 'devices.db')
sqlalchemy_database_url = f"sqlite:///{db_path}"

# Load in config object
with open(os.path.join(base_path, "wapi", "config.yaml"), 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

import logging
import os

import yaml

# Get environment variable for environment - default to DEV if not found
# TODO: Use dot-env to make this work
environment = os.getenv("ENV", "local")

if environment == "unittest":
    db_path = os.path.join("test_data/sqlite/devices.db")
elif environment in ("DEV", "PROD"):
    base_path = os.path.join("/home", "pi", environment, "smarty-lamps")
    db_path = os.path.join('/home', 'sqlite', 'live', 'devices.db')
else:
    # For local testing, set an empty base path
    db_path = os.path.join("test_data/sqlite/devices.db")
    base_path = ""

sqlalchemy_database_url = f"sqlite:///{db_path}"

# Load in config object
with open(os.path.join(base_path, "wapi", "config.yaml"), 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

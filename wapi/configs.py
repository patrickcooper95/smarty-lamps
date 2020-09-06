import os

import yaml

# Get environment variable for environment - default to PROD if not found
environment = os.getenv("ENV", "PROD")
base_path = os.path.join("/home", "pi", environment, "smarty-lamps")
db_path = os.path.join('/home', 'sqlite', 'live', 'devices.db')


# Load in config object
with open(os.path.join(base_path, "wapi", "config.yaml"), 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

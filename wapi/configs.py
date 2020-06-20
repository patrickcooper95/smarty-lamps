import yaml


# Load in config object
with open("/home/pi/WAPI/smarty-lamps/config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

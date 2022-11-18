import yaml


with open("config.yaml", "r") as config_file:
    Config = yaml.safe_load(config_file)


def get_nyct_feed(service: str):
    """Determine the feed endpoint for selected service."""

    service_mapping = {
        "lexington_ave_feed": ["4", "5", "6"],
        "seventh_ave_feed": ["1", "2", "3"],
        "flushing_feed": ["7"],
        "broadway_feed": ["N", "Q", "R", "W"]
    }

    for feed, services in service_mapping.items():
        if service in services:
            return feed
    else:
        raise ValueError("Services specified does not have a configured feed.")

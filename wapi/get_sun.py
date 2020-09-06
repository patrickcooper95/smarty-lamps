import datetime, os

import requests

import wapi.configs as configs

config = configs.config


def get_sun():
    """Get sunrise and sunset time."""

    url = f"{config['BASE_URL']}zip={config['New York']['ZIP']}" \
        f"&appid={config['KEY']}"

    weather = requests.get(url).json()

    sunrise = (datetime.datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M:%S'))
    sunset = (datetime.datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M:%S'))

    # TODO: pickle to file
    with open(os.path.join(configs.base_path, "wapi", "sun.txt"), 'w') as file:
        file.write(f"{sunrise},{sunset}")
    file.close()

import os
from pulsefire.clients import RiotAPIClient

from src.util import config

# todo: move the key somewhere else -> the config
client = RiotAPIClient(default_headers={"X-Riot-Token": config.RIOT_API_KEY})

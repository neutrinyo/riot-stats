import os
from pulsefire.clients import RiotAPIClient

# todo: move the key somewhere else
client = RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]})

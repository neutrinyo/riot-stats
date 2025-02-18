import os

RIOT_API_KEY = os.environ["RIOT_API_KEY"]

# |-----------------------------------------------------DATABASE--------------------------------------------------------|

# todo - move the db credentials to a safe place, hardcoding will do for early development
DATABASE_URL = 'postgresql://admin:admin@localhost/riot_stats_db'

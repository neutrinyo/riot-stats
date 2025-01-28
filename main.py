import argparse
import re

def parse_username(username: str) -> str:
    user_match = re.match('^[a-zA-Z0-9]{3,16}#[a-zA-Z0-9]{3,5}$', username)

    if user_match:
        game_name, tag_line = user_match.string.split("#")
        return game_name, tag_line

    raise ValueError("Provided username is invalid - please refer to Riot ID guidelines for details.")

parser = argparse.ArgumentParser(
    prog='riot_stats',
    description='Statistical and visual analysis of League of Legends match/player data.'
)

parser.add_argument('-u', '--user')
parser.add_argument('-d', '--data')

args = parser.parse_args()
name, tag = parse_username(args.user)
print(name, tag)

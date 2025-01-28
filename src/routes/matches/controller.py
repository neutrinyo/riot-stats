import re
from pulsefire.schemas import RiotAPISchema

def parse_username(username: str) -> list[str]:
    user_match = re.match('^[a-zA-Z0-9]{3,16}#[a-zA-Z0-9]{3,5}$', username)

    if user_match:
        game_name, tag_line = user_match.string.split("#")
        return [game_name, tag_line]

    raise ValueError("Provided username is invalid - please refer to Riot ID guidelines for details.")

def get_champions_list(self, match_data: RiotAPISchema.LolMatchV5Match) -> list[str]:
    champions = []
    for participant in match_data['info']['participants']:
        champions.append(participant['championName'])

    return champions

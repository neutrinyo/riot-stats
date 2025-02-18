# |----------------------------------------------------OUTSIDE IMPORTS--------------------------------------------------|

from fastapi import APIRouter
from pulsefire.schemas import RiotAPISchema
from typing_extensions import Self
from pydantic import BaseModel, ValidationError, model_validator
import pdb

# |-----------------------------------------------------IN-APP IMPORTS--------------------------------------------------|
import src.routes.matches.controller as controller
from src.util.riot_client import client
import src.routes.users.main as users # chyba przeniose to do wyzszego punktu, zalezy czy sie w ogole przyda

# todo - config z regionem, request bodies przy wiekszych datasetach? (chyba ze i tak uzyje pulsefirowych typow)
# moze sie przydac participant enum zeby latwo skakac pomiedzy id, puuid i nickiem - nawet nie enum tylko actual object with the data i need
# wykresy - heatmap smierci per rola? pretty cool i think

# |------------------------------------------------REQUEST/RESPONSE BODIES----------------------------------------------|

class MatchData(BaseModel):
    lol_match: RiotAPISchema.LolMatchV5Match
    timeline: RiotAPISchema.LolMatchV5MatchTimeline
    filter_attribute: str
    game_mode: str

    @model_validator(mode='after')
    def filter_timeline_events_by_attribute(self) -> Self:
    # todo - zmodyfikowac by mozna bylo filtrowac tez po wartosci samego atrybutu a nie tylko jego istnieniu.
        for frame in self.timeline['info']['frames']:
            filtered_events = list()
            for event in frame['events']:
                if self.filter_attribute in event:
                    filtered_events.append(event)
            frame['events'] = filtered_events
    
        return self

    @model_validator(mode='after')
    def filter_matches_by_game_type(self) -> Self:
        if self.lol_match['info']['gameMode'] != self.game_mode:
            raise ValidationError("Match has a different game mode than requested or the provided game mode value is invalid.")
        
        return self

# |----------------------------------------------------GLOBAL METHODS---------------------------------------------------|
# todo: move to another file? maybe

async def fetch_matches(region: str = "europe", name: str = "", count: int = 20) -> list[str]:
    account = await users.fetch_user_data(region, name)
    matches = await client.get_lol_match_v5_match_ids_by_puuid(region="europe", puuid=account["puuid"], 
                                                               queries={"start": 0, "count": count})
    return matches


# |----------------------------------------------------- ENDPOINTS -----------------------------------------------------|

router = APIRouter(
    prefix="/matches",
    tags=["Match"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_matches(region: str = "europe", name: str = "", count: int = 20) -> list[str]:
    matches = await fetch_matches(region, name, count)
    return matches

@router.get("/data/")
async def get_match_data(region: str = "europe", name: str = "", count: int = 7, filter_attribute: str = "position", game_mode: str = "CLASSIC") -> list[MatchData]:
    # todo - move default vals into config, zrobic tak zeby sfetchowac tyle meczy ile chce danego typu.
    matches = await fetch_matches(region, name, count)
    matches_data = list()

    for match_id in matches:
        match_timeline = await client.get_lol_match_v5_match_timeline(region=region, id=match_id)
        lol_match = await client.get_lol_match_v5_match(region=region, id=match_id)
        lol_match = controller.patch_bounty_gold(lol_match)
        try:
            matches_data.append(
                MatchData(lol_match=lol_match, timeline=match_timeline, filter_attribute=filter_attribute, game_mode=game_mode)
            )
        except ValidationError as e:
            pass

    return matches_data

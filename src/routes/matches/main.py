# |----------------------------------------------------OUTSIDE IMPORTS--------------------------------------------------|

from fastapi import APIRouter
from pulsefire.schemas import RiotAPISchema
from pydantic import BaseModel

# |-----------------------------------------------------IN-APP IMPORTS--------------------------------------------------|

from src.util.riot_client import client
from src.routes.users.main import fetch_user_data
from .controller import patch_bounty_gold

# todo - config z regionem, request bodies przy wiekszych datasetach? (chyba ze i tak uzyje pulsefirowych typow)
# moze sie przydac participant enum zeby latwo skakac pomiedzy id, puuid i nickiem - nawet nie enum tylko actual object with the data i need
# wykresy - heatmap smierci per rola? pretty cool i think

# |------------------------------------------------REQUEST/RESPONSE BODIES----------------------------------------------|

class MatchData(BaseModel):
    lol_match: RiotAPISchema.LolMatchV5Match
    timeline: RiotAPISchema.LolMatchV5MatchTimeline


# |----------------------------------------------------GLOBAL METHODS---------------------------------------------------|

async def fetch_matches(region: str = "europe", name: str = "", count: int = 20) -> list[str]:
    account = await fetch_user_data(region, name)
    matches = await client.get_lol_match_v5_match_ids_by_puuid(
                    region="europe", puuid=account["puuid"], queries={"start": 0, "count": count})
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
async def get_match_data(region: str = "europe", name: str = "", count: int = 20) -> list[MatchData]:
    matches = await fetch_matches(region, name, count)
    matches_data = []

    for match_id in matches:
        match_timeline = await client.get_lol_match_v5_match_timeline(region="europe", id=match_id)
        lol_match = await client.get_lol_match_v5_match(region="europe", id=match_id)
        lol_match = patch_bounty_gold(lol_match)
        matches_data.append(
            MatchData(lol_match=lol_match, timeline=match_timeline)
        )

    return matches_data

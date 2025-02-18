# |----------------------------------------------------OUTSIDE IMPORTS--------------------------------------------------|

from fastapi import APIRouter
from pulsefire.schemas import RiotAPISchema

# |-----------------------------------------------------IN-APP IMPORTS--------------------------------------------------|

import src.routes.users.controller as controller
from src.util.riot_client import client

# |------------------------------------------------REQUEST/RESPONSE BODIES----------------------------------------------|



# |----------------------------------------------------GLOBAL METHODS---------------------------------------------------|

async def fetch_user_data(region: str = "europe", names: list = "") -> RiotAPISchema.AccountV1Account:
    game_name, tag_line = controller.parse_username(names)
    account = await client.get_account_v1_by_riot_id(region=region, game_name=game_name, tag_line=tag_line)
    return account

# |----------------------------------------------------- ENDPOINTS -----------------------------------------------------|

router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_multiple_user_data():
    return "Dummy endpoint."

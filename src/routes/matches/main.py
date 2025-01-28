from fastapi import APIRouter

from .controller import get_champions_list, parse_username
from src.util.riot_client import client

router = APIRouter(
    prefix="/matches",
    tags=["Match"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def fetch_user(username: str = ""):
    game_name, tag_line = parse_username(username)
    account = await client.get_account_v1_by_riot_id(region="europe", game_name=game_name, tag_line=tag_line)
    return account

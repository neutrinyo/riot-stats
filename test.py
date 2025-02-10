from pulsefire.clients import RiotAPIClient
import pdb
import asyncio
import os

async def fn():
    async with RiotAPIClient(default_headers={"X-Riot-Token": 'RGAPI-4d6776b4-479b-483d-8e6d-19a28cb0d801'}) as client:
        account = await client.get_account_v1_by_riot_id(region="europe", game_name="twojstary2komary", tag_line="win")
        matches = await client.get_lol_match_v5_match_ids_by_puuid(region="europe", puuid=account["puuid"], queries={"start": 0, "count": 20})

        for match_id in matches:
            match_timeline = await client.get_lol_match_v5_match_timeline(region="europe", id=match_id)
            match = await client.get_lol_match_v5_match(region="europe", id=match_id)
            pass

asyncio.run(fn())

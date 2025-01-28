from pulsefire.clients import RiotAPIClient
import pdb
import asyncio

async def fn():
    async with RiotAPIClient(default_headers={"X-Riot-Token":"RGAPI-4555583b-8b75-4d6c-8782-25e651f34e0a"}) as client:
        account = await client.get_account_v1_by_riot_id(region="europe", game_name="twojstary2komary", tag_line="win")
        matches = await client.get_lol_match_v5_match_ids_by_puuid(region="europe", puuid=account["puuid"], queries={"start": 0, "count": 20})

        for match_id in matches:
            match_timeline = await client.get_lol_match_v5_match_timeline(region="europe", id=match_id)
            match = await client.get_lol_match_v5_match(region="europe", id=match_id)
            pass

asyncio.run(fn())

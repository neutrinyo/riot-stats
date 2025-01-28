import os

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pulsefire.clients import RiotAPIClient

client = RiotAPIClient(default_headers={"X-Riot-Token": os.environ["RIOT_API_KEY"]})

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with client:
        yield

app = FastAPI(lifespan=lifespan)

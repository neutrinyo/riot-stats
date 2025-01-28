import re

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.routes.matches.main import router
from src.util.riot_client import client


# create lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with client:
        yield

# init the app itself using the lifespan, include routers, create main route
app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/")
def main_function():
    return {"Hello": "World"}

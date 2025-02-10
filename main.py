from contextlib import asynccontextmanager
from fastapi import FastAPI

import src.routes.matches.main as matches
import src.routes.users.main as users
from src.util.riot_client import client


# create lifespan function
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    async with client:
        yield

# init the app itself using the lifespan, include routers, create main route
app = FastAPI(lifespan=lifespan)
app.include_router(matches.router)
app.include_router(users.router)

@app.get("/")
def main_function():
    return "Available main endpoints: /matches"

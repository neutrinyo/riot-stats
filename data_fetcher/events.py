from . import app, client

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    account = await client.get_account_v1_by_riot_id(region="europe", game_name="twojstary2komary", tag_line="win")
    return account

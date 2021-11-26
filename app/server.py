from fastapi import FastAPI
from fastapi.params import Body
from shems import Match
from db import get_player_id, push_match

app = FastAPI()

@app.get(
    '/match'
    #response_model=Match
)
async def get_match(matchid: int):
    '''Возвращяет матч'''
    id = await get_player_id('s1mple', 'ffff')
    
    return {"ff": id}

@app.post(
    '/pushmatch'
)
async def push_match(match: Match = Body(...)):
    '''Закидывает матчи в бд'''
    
    push_match(match)
    
    return {"status":8}
    

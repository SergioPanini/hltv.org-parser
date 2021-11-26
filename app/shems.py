from typing import List
from pydantic import BaseModel

class Player(BaseModel):
    '''Класс игрока'''
    name: str
    url: str

class Team(BaseModel):
    '''Класс команды'''
    name: str

class Player_stat(BaseModel):
    '''Класс статистики игрока'''
    date: float
    KD: float
    ADR: float
    KAST: float
    Raiting: float
    player: Player

class Side(BaseModel):
    '''Класс стороны'''
    t: List[Player_stat]
    ct: List[Player_stat]
    
class Map_stat(BaseModel):
    '''Класс статистики карты'''
    name: str
    t1_score: int
    t2_score: int
    team1_stat: Side = None
    team2_stat: Side = None
    
class Match(BaseModel):
    '''Класс матча'''
    id: int
    date: float
    team1: Team
    team2: Team
    match_type: str
    maps: List[Map_stat]

class Matches(BaseModel):
    '''Класс матчей'''
    
    matches: List[Match]
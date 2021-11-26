
from asyncpg.types import Attribute
import asyncpg
import asyncio

from settings import DB
from shems import Match
from datetime import datetime

async def init():
    '''Создание таблиц'''
    
    init_scripts = [
        "CREATE TABLE IF NOT EXISTS players (\
            id serial NOT NULL,\
            name varchar(40) NOT NULL,\
            url text NOT NULL,\
            PRIMARY KEY (id)\
        );",
        "CREATE TABLE IF NOT EXISTS teams (\
            id serial NOT NULL,\
            name varchar(40) NOT NULL,\
            PRIMARY KEY (id)\
        );",
        "CREATE TABLE IF NOT EXISTS matches (\
            id serial NOT NULL,\
            date timestamp NOT NULL,\
            team1_id integer NOT NULL,\
            team2_id integer NOT NULL,\
            match_type varchar(40) NOT NULL,\
            PRIMARY KEY (id),\
            FOREIGN KEY (team1_id) REFERENCES teams(id) ON DELETE CASCADE,\
            FOREIGN KEY (team2_id) REFERENCES teams(id) ON DELETE CASCADE\
        );",
        "CREATE TABLE IF NOT EXISTS map_stats (\
            id serial NOT NULL,\
            match_id integer NOT NULL,\
            map_name varchar(40) NOT NULL,\
            t1_score integer NOT NULL,\
            t2_score integer NOT NULL,\
            PRIMARY KEY (id),\
            FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE\
        );",
        "CREATE TABLE IF NOT EXISTS player_stats (\
            id serial NOT NULL,\
            map_stat_id integer NOT NULL,\
            player_id  integer NOT NULL,\
            team_id integer NOT NULL,\
            side varchar(40) NOT NULL,\
            KD float NOT NULL,\
            ADR float NOT NULL,\
            KAST float NOT NULL,\
            Raiting float NOT NULL,\
            PRIMARY KEY (id),\
            FOREIGN KEY (map_stat_id) REFERENCES map_stat(id) ON DELETE CASCADE,\
            FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,\
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE\
        );"
    ]
    
    conn = await asyncpg.connect(DB)
    for i in init_scripts:
        await conn.execute(i)

async def get_player_id(name: str, url: str) -> int:
    '''Получаем id игрока'''
    
    conn = await asyncpg.connect(DB)
    records = await conn.fetch("SELECT id FROM players WHERE players.name = $1", name)
    if not records:
        return await conn.fetch(
            "INSERT INTO players(name, url) VALUES($1, $2) RETURNING id",
            name,
            url
        )
    return records[0]['id']

async def get_team_id(name: str):
    '''Вставляет команду'''

    conn = await asyncpg.connect(DB)
    records = await conn.fetch("SELECT id FROM teams WHERE teams.name = $1", name)
    if not records:
        return await conn.fetch(
            "INSERT INTO teams(name) VALUES($1) RETURNING id",
            name,
        )
    return records[0]['id']

async def get_match_id(
    date: float,
    team1_id: int,
    team2_id: int,
    match_type: str
):
    '''Вставляет матч'''
    
    conn = await asyncpg.connect(DB)
    records = await conn.fetch(
        "INSER INTO matches(\
            date,\
            team1_id,\
            team2_id,\
            match_type\
            ) VALUES($1, $2, $3, $4) RETURNING id",
        date,
        team1_id, team2_id, match_type
    )

    return records[0]['id']

async def insert_map_stat(
    match_id: int,
    map_name: str,
    t1_score: int,
    t2_score: int
):
    '''Вставляет статистику матча'''
    pass

async def insert_player_stat(
    map_stat_id: int,
    player_id: int,
    team_id: int,
    side: str,
    KD: float,
    ADR: float,
    KAST: float,
    Raiting: float
):
    '''Вставляет статистику игрока за определенную сторону'''
    
    conn = asyncpg.connect(DB)
    records = await conn.fetch(
        "INSERT INTO player_stat(\
            mpa_stat_id,\
            player_id,\
            team_id,\
            side,\
            KD,\
            ADR,\
            KAST,\
            Raiting\
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id")
    

async def push_match(match:  Match):
    '''Вставляет матч в бд'''
    
    team1_id = await get_team_id(match.team1.name)
    team2_id = await get_team_id(match.team2.name)
    
    match_id = get_match_id(datetime.timestamp(), team1_id, team2_id, match.match_type)
    
    for map_ in match.maps:
        map_stat_id = await get_match_id(match_id, map_.name, map_.t1_score, map_.t2_score)
        for n in range(1, 2):
            team = map_.__getattribute__(f"team{n}_stat")
            
            for side in ['t', 'ct']:
                for player_stat in team.__getattribute__(side):
                    
                    player_id = await get_player_id(player_stat.player.name, player_stat.player.url)
                    
                    await insert_player_stat(
                        map_stat_id,
                        player_id,
                        team_id=Attribute(f"team{n}_id"),
                        side=side,
                        KD=player_stat.KD,
                        ADR=player_stat.ADR,
                        KAST=player_stat.KAST,
                        Raiting=player_stat.Raiting
                        )


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(init())

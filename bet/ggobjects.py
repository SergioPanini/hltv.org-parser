from pydantic import BaseModel


class Match(BaseModel):
    '''Класс матча'''

    team1_name: str
    team2_name: str

    team1_ratio: float
    team2_ratio: float

    url: str
    event_url: str
    parse_datetime: str
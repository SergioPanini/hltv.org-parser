from pydantic import BaseModel


class Match(BaseModel):
    '''Класс матча'''
    event: str
    team_left_name: str
    team_right_name: str

    team_left_ratio: float
    team_right_ratio: float

    url: str
    match_time: str
    parser_datetime: str
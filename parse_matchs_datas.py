from os import kill
import bs4
import requests
import pandas as pd
from time import sleep
import random

from typing import Tuple, List


class Player():
    '''Класс киберспортсмера'''

    nick: str = None
    url: str = None

    Kills: int = None
    Death: int = None

    K_D: int = None
    ADR: float = None
    KAST: float = None
    Raiting: float = None

class TeamStat():
    '''Класс статистика игры за какую то сторону'''

    tstat: List[Player] = []
    ctstat: List[Player] = []

class Map():
    '''Класс карты'''

    name: str = None

    team1_score: str = '-'
    team2_score: str = '-'

    #Команда, которая выбрала эту карту
    pick_team: str = None

    team1_stat: TeamStat = TeamStat()
    team1_stat: TeamStat = TeamStat()

    @property
    def is_played(self):
        '''Проверяет была ли сыграна карту'''

        if self.team1_score == '-' and self.team2_score == '-':
            return False
        
        return True
    
    def __repr__(self):

        return f'\n Name: {self.name}, team1_score: {self.team1_score}, team2_score: {self.team2_score}, pick_team: {self.pick_team}'



def _push_request(URL:  str, data=None, repeat_delay: int=1, max_delay: int=10) -> str:
    '''Отправляет запрос на URL'''

    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'content-type': 'text/html;charset=utf-8'
    }

    #Задержка против блокировки
    sleep(random.randint(1, 30)/10)

    repeat = 1
    while True:
        
        #Отправляем запрос
        response = requests.get(URL, headers=headers)

        print('[Push] Request url: ', URL)
        print('[Push] Response status code: ', response.status_code)
        print('[Push] Repeat: ', repeat)

        #Если ответ не OK
        if response.status_code != 200:
            
            #Высчитываем задержку
            delay = repeat * repeat_delay if repeat * repeat_delay < max_delay else max_delay
            sleep(delay)
            repeat +=1
        
        else:
            break

    return response.text

def _find_event_and_date(html_page: str) -> Tuple[str, str]:
    '''Ищет мероприятие и дату мероприятия в html странице'''
    
    soup = bs4.BeautifulSoup(html_page, 'html.parser')
    info_block = soup.find(class_='teamsBox')

    event = info_block.find(class_='timeAndEvent').find(class_='event').text
    date = info_block.find(class_='timeAndEvent').find(class_='date').text

    return event, date

def _find_maps(html_page: str) -> List[Map]:
    '''Ишет карты в html странице'''

    soup = bs4.BeautifulSoup(html_page, 'html.parser')

    mapholder = soup.find_all(class_='mapholder')

    mapsholder_list = list(mapholder)

    result_maps_list = []

    for map in mapsholder_list:
        
        obj_map = Map()
        
        obj_map.name = map.find(class_='mapname').text
        
        results_left = map.find(class_='results-left')
        results_right = map.find(class_='results-right')
        
        #Проверяем что карта игралась в матче. Если нет, то team1_score и team2_score по умалчанию '-'
        if results_left and results_left:

            #Ищем скоры
            obj_map.team1_score = results_left.find(class_='results-team-score').text
            obj_map.team2_score = results_right.find(class_='results-team-score').text

            #Ищем кто выбрал эту карту
            if 'pick' in results_left.get('class'):
                obj_map.pick_team = 'team1'

            if 'pick' in results_right.get('class'):
                obj_map.pick_team = 'team2'


        result_maps_list.append(obj_map)
    
    return result_maps_list


def _find_teams_scores(html_page: str) -> Tuple[str, str]:
    '''Ищет счет первой и второй команд'''

    soup = bs4.BeautifulSoup(html_page, 'html.parser')
    
    team1_score = soup.find(class_='team1-gradient').find(class_='won').text if soup.find(class_='team1-gradient').find(class_='won') else soup.find(class_='team1-gradient').find(class_='lost').text 
    team2_score = soup.find(class_='team2-gradient').find(class_='won').text if soup.find(class_='team2-gradient').find(class_='won') else soup.find(class_='team2-gradient').find(class_='lost').text 

    return team1_score, team2_score

def _find_tesms_names(html_page: str) -> Tuple[str, str]:
    '''Ищет названия первой и второй команды'''

    soup = bs4.BeautifulSoup(html_page, 'html.parser')
    
    team_1 = soup.find(class_='team1-gradient').find(class_='teamName').text
    team_2 = soup.find(class_='team2-gradient').find(class_='teamName').text

    return team_1, team_2



def main(URL: str = None, repeat_delay=1, max_delay = 10, csv_file=None):
    #Создаем или открываем файл для записи данных
    if csv_file:
        df = pd.read_csv(csv_file, sep=',')
    
    else:
        df = pd.DataFrame(columns=['date', 'team1', 'team2', 'result_score', 'event', 'map_1', 'map_2', 'map_3', 'team_1_pick', 'team_1_pick', 'map_1_score', 'map_2_score', 'map_3_score', 'match_history', 'match_url'])


    match_page = _push_request(URL=URL, repeat_delay=repeat_delay, max_delay=max_delay)

    event, date = _find_event_and_date(match_page)

    team1_score, team2_score = _find_teams_scores(match_page)
    
    team1_name, team2_name = _find_tesms_names(match_page)

    
    maps_list = _find_maps(match_page)

    soup = bs4.BeautifulSoup(match_page, 'html.parser')

    pick_history = soup.find_all(class_='veto-box')[-1]
    print('pick_history: ', pick_history.text)
    #print('mph: ', results_left.get('class'))

    _get_match_stat(match_page)

    print('[INFO] Event: ', date)
    print('[INFO] Date: ', event)
    print('[INFO] Team1: ', team1_name)
    print('[INFO] Team2: ', team2_name)
    print('[INFO] Team1 score: ', team1_score)
    print('[INFO] Team2: score', team2_score)
    print('[INFO] Maps: ', maps_list)
    


if __name__ == '__main__':
    main('https://www.hltv.org/matches/2350366/furia-vs-teamone-esl-pro-league-season-14')
'''Тут хранятся объекты, которые оспользуются для парсинга'''

from typing import List, Dict, Tuple
import bs4
from numpy import mat

class Player():
    '''Класс киберспортсмера'''

    nick: str = None
    url: str = None

    K_D: str = None
    ADR: float = None
    KAST: float = None
    Rating: float = None

    def __repr__(self) -> dict:
        return str(self.get())

    def get(self) -> dict:
        '''Возвращяет поля игрока в виде словаря'''
        
        return {
            'Nick': self.nick,
            'K-D': self.K_D,
            'ADR': self.ADR,
            'KASR': self.KAST,
            'Rating': self.Rating,
            'url': self.url
            }


class TeamStat():
    '''Класс статистика игры за какую то сторону'''

    tstat: List[Player] = []
    ctstat: List[Player] = []

    def __repr__(self) -> dict:
        return str({'tstat': self.tstat, 'ctstat': self.ctstat})

class Map():
    '''Класс карты'''

    name: str = None

    team1_score: str = '-'
    team2_score: str = '-'

    #Команда, которая выбрала эту карту
    pick_team: str = None

    team1_stat: TeamStat = TeamStat()
    team2_stat: TeamStat = TeamStat()

    @property
    def is_played(self):
        '''Проверяет была ли сыграна карту'''

        if self.team1_score == '-' and self.team2_score == '-':
            return False
        
        return True
    
    def __repr__(self) -> dict:

        return str({
            'map': self.name,
            'team1_score': self.team1_score,
            'team2_score': self.team2_score,
            'pick_team': self.pick_team,
            'team1_stat': self.team1_stat,
            'team2_stat': self.team2_stat
            })


class Match:
    '''Класс матча, который хранит все нужные данные'''

    date: str = None
    event: str = None

    teame_name: str = None
    team2_name: str = None

    team1_score: str = None
    team2_score: str = None

    maps: List[Map] = []

    def __init__(self, html_page: str):
        '''Ищет все нужные данные матча'''
        
        self.event, self.date = self._find_event_and_date(html_page)
        self.team1_score, self.team2_score = self._find_teams_scores(html_page)
        self.team1_name, self.team2_name = self._find_tesms_names(html_page)
        self.maps = self._find_maps(html_page)
    
    def __repr__(self) -> str:
        return str({
            'data': self.date,
            'event': self.event,
            'team1_name': self.team1_name,
            'team2_name': self.team2_name,
            'team1_score': self.team1_score,
            'team2_score': self.team2_score,
            'maps': self.maps
        })
        
    def _find_event_and_date(self, html_page: str) -> Tuple[str, str]:
        '''Ищет мероприятие и дату мероприятия в html странице'''

        soup = bs4.BeautifulSoup(html_page, 'html.parser')
        info_block = soup.find(class_='teamsBox')

        event = info_block.find(class_='timeAndEvent').find(class_='event').text
        date = info_block.find(class_='timeAndEvent').find(class_='date').text

        return event, date

    def _find_maps(self, html_page: str) -> List[Map]:
        '''Ишет карты в html странице'''

        soup = bs4.BeautifulSoup(html_page, 'html.parser')

        mapholder = soup.find_all(class_='mapholder')

        mapsholder_list = list(mapholder)

        result_maps_list: List[Map] = []

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


        #Получаем статистику матчей которые были сыграны
        map_stat = self._get_match_stat(html_page)
        for i, stat in enumerate (map_stat):
            result_maps_list[i].team1_stat = stat[0]
            result_maps_list[i].team2_stat = stat[1]


        return result_maps_list


    def _find_teams_scores(self, html_page: str) -> Tuple[str, str]:
        '''Ищет счет первой и второй команд'''

        soup = bs4.BeautifulSoup(html_page, 'html.parser')

        team1_score = soup.find(class_='team1-gradient').find(class_='won').text if soup.find(class_='team1-gradient').find(class_='won') else soup.find(class_='team1-gradient').find(class_='lost').text 
        team2_score = soup.find(class_='team2-gradient').find(class_='won').text if soup.find(class_='team2-gradient').find(class_='won') else soup.find(class_='team2-gradient').find(class_='lost').text 

        return team1_score, team2_score

    def _find_tesms_names(self, html_page: str) -> Tuple[str, str]:
        '''Ищет названия первой и второй команды'''

        soup = bs4.BeautifulSoup(html_page, 'html.parser')

        team_1 = soup.find(class_='team1-gradient').find(class_='teamName').text
        team_2 = soup.find(class_='team2-gradient').find(class_='teamName').text

        return team_1, team_2

    def _get_player_stat(self, html_side_stat):
        '''Ищет статистику игрока для какой либо стороны'''

        obj_player = Player()
        obj_player.nick = html_side_stat.find(class_='player-nick').text
        obj_player.K_D = html_side_stat.find(class_='kd').text
        obj_player.ADR = float(html_side_stat.find(class_='adr').text)
        obj_player.KAST = float(html_side_stat.find(class_='kast').text.replace('%', ''))
        obj_player.Rating = float(html_side_stat.find(class_='rating').text)
        obj_player.url = 'https://www.hltv.org' + html_side_stat.find(class_='no-maps-indicator-offset').get('href')

        return obj_player


    def _get_match_stat(self, html_page: str) -> List[Dict[TeamStat, TeamStat]]:
        '''Ищет статистику матча'''

        soup = bs4.BeautifulSoup(html_page, 'html.parser')

        stat_block = soup.find(class_='matchstats')

        maps = stat_block.find_all(class_='stats-content')[1:]

        result = []

        for map_ in maps:

            obj_team1_stat = TeamStat()
            obj_team2_stat = TeamStat()

            #Ищем команды
            team1_stat, team2_stat = map_.find_all(class_='table')[1:3], map_.find_all(class_='table')[4:]

            #Ищем кт и т стороны для каждой команды 
            team1_ctstat, team1_tstat, team2_ctstat, team2_tstat = team1_stat[0], team1_stat[1], team2_stat[0], team1_stat[1]

            #Ищем статистику для первой команды для т стороны
            for player in team1_tstat.find_all('tr')[1:]:
                obj_team1_stat.tstat.append(self._get_player_stat(player))

            #Ищем статистику для первой команды для кт стороны
            for player in team1_ctstat.find_all('tr')[1:]:
                obj_team1_stat.ctstat.append(self._get_player_stat(player))

            #Ищем статистику для второй команды для т стороны
            for player in team2_tstat.find_all('tr')[1:]:
                obj_team2_stat.tstat.append(self._get_player_stat(player))

            #Ищем статистику для второй команды для кт стороны
            for player in team2_ctstat.find_all('tr')[1:]:
                obj_team2_stat.ctstat.append(self._get_player_stat(player))

            result.append((obj_team1_stat, obj_team2_stat))

        return result



class MatchCreator:
    '''Создает матч'''

    def __new__(cls, html_page: str):

        try:
        
            match = Match(html_page)
        
            return match
        
        except:
            return None
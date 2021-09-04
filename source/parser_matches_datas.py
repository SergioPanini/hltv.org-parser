import bs4
from numpy import mat
import requests
import pandas as pd
from time import sleep
import random

from objects import MatchCreator, Match


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

def _write_match_to_df(df: pd.DataFrame, match: Match, match_url: str):
    
    for i, map_ in enumerate(match.maps):

        side = 'ct'
        team_name = match.team1_name
        for player in map_.team1_stat.ctstat:
                    
            data_dict = {
            'match_url': match_url,
            'date': match.date,
            'event': match.event,
            'team1_name': match.team1_name,
            'team2_name': match.team2_name,
            'match_team1_score': match.team1_score,
            'match_team2_score': match.team2_score,
            'map_name':map_.name,
            'map_pick_team': map_.pick_team,
            'side':side,
            'team_name': team_name,
            'nick':player.nick,
            'player_url':player.url,
            'K_D':player.K_D,
            'ADR':player.ADR,
            'KAST':player.KAST,
            'Rating':player.Rating
            }

            df = df.append(data_dict, ignore_index=True)

        side = 't'
        team_name = match.team1_name
        for player in map_.team1_stat.tstat:
                    
            data_dict = {
            'match_url': match_url,
            'date': match.date,
            'event': match.event,
            'team1_name': match.team1_name,
            'team2_name': match.team2_name,
            'match_team1_score': match.team1_score,
            'match_team2_score': match.team2_score,
            'map_name':map_.name,
            'map_pick_team': map_.pick_team,
            'side':side,
            'team_name': team_name,
            'nick':player.nick,
            'player_url':player.url,
            'K_D':player.K_D,
            'ADR':player.ADR,
            'KAST':player.KAST,
            'Rating':player.Rating
            }

            df = df.append(data_dict, ignore_index=True)

        side = 'ct'
        team_name = match.team2_name
        for player in map_.team2_stat.ctstat:
                    
            data_dict = {
            'match_url': match_url,
            'date': match.date,
            'event': match.event,
            'team1_name': match.team1_name,
            'team2_name': match.team2_name,
            'match_team1_score': match.team1_score,
            'match_team2_score': match.team2_score,
            'map_name':map_.name,
            'map_pick_team': map_.pick_team,
            'side':side,
            'team_name': team_name,
            'nick':player.nick,
            'player_url':player.url,
            'K_D':player.K_D,
            'ADR':player.ADR,
            'KAST':player.KAST,
            'Rating':player.Rating
            }

            df = df.append(data_dict, ignore_index=True)

        side = 't'
        team_name = match.team2_name
        for player in map_.team2_stat.ctstat:
                    
            data_dict = {
            'match_url': match_url,
            'date': match.date,
            'event': match.event,
            'team1_name': match.team1_name,
            'team2_name': match.team2_name,
            'match_team1_score': match.team1_score,
            'match_team2_score': match.team2_score,
            'map_name':map_.name,
            'map_pick_team': map_.pick_team,
            'side':side,
            'team_name': team_name,
            'nick':player.nick,
            'player_url':player.url,
            'K_D':player.K_D,
            'ADR':player.ADR,
            'KAST':player.KAST,
            'Rating':player.Rating
            }

            df = df.append(data_dict, ignore_index=True)

    return df




def main(file_name: str, repeat_delay=1, max_delay = 10, csv_file=None):
    
    #Создаем или открываем файл для дозаписи данных
    if csv_file:
        df = pd.read_csv(csv_file, sep=',')
    
    else:
        df = pd.DataFrame(columns=['match_url'])

    urls_file = open(file_name, 'r')
    error_file = open('error_urls_file.log', 'a')
    
    print('[INFO] _______Start Work_______')

    while True:
        url = urls_file.readline()

        #ПРоверяем что мы закончили читать файл со ссылками
        if not url:
            print('end urls file')
            df.to_csv('matches.csv', sep=',', index=False)
            break
        
        #Проверяем что этого адреса нет в таблице
        if not (True in list(df['match_url'] == url)):

            #Собираем данные 
            try:
                match_page = _push_request(url)
            except:
                print('[WARNING] Problems with url: ', url)
                error_file.write(url)
                continue

            match_stat = MatchCreator(match_page)

            if match_page:
                print('[INFO] Write url: ', url)
                df = _write_match_to_df(df, match_stat, url)
            
            else:
                print('[WARNING] Problems with url: ', url)
                error_file.write(url)

    print('[INFO] End urls file')
    print('[INFO] _______END Work_______')  



if __name__ == '__main__':
    main('../urls.txt')
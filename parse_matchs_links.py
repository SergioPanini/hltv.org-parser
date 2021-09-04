import requests
import bs4
import pandas as pd
from time import sleep, time
import random


def parse_matches(offset_start=0, offset_stop = None, repeat_delay=1, max_delay = 10, csv_file=None):
    '''Функция парсит матчи и сохраняет их в csv файл'''

    URL = r'https://www.hltv.org/results'



    #Создаем или открываем файл для записи данных
    if csv_file:
        df = pd.read_csv(csv_file, sep=',')
    
    else:
        df = pd.DataFrame(columns=['date', 'team1', 'team2', 'result_score', 'event', 'match_url'])

    #Получаем все кол-во матчей
    response_text = _push_request(URL, repeat_delay=repeat_delay, max_delay=max_delay)
    soup = bs4.BeautifulSoup(response_text, 'html.parser')

    result_matchs_count = int(soup.find(class_='pagination-data').text.split(' ')[-2])
    
    if not offset_stop or offset_stop > result_matchs_count:
        offset_stop = result_matchs_count
    
    print('[INFO] Pagination: ', result_matchs_count)
    print('[INFO] Offset start: ', offset_start)
    print('[INFO] Offset stop: ', offset_stop)
    

    for i in range((offset_stop - offset_start) // 100):
        newURL = URL + f'?offset={offset_start + i * 100}'

        response_text = _push_request(newURL, repeat_delay=repeat_delay, max_delay=max_delay)

        soup = bs4.BeautifulSoup(response_text, 'html.parser')

        #Находим блок в сезультатами
        results_all = soup.find_all(class_='results-all')[-1]

        #Находим даты, в которых были матчи
        results_sublist = results_all.find_all(class_='results-sublist')
    
        #Находим матчи и саму дату
        for sublist in results_sublist:
            date = sublist.find(class_='standard-headline').text
            matches = sublist.find_all(class_='result-con')

            print('[INFO] Date: ', date)

            #Находим названия матчей
            for i, match in enumerate(matches):
                teams = [team.text for team in match.find_all(class_='team')]
                event_name = match.find(class_='event-name').text
                result_score = match.find(class_='result-score').text
                match_url = 'hltv.org' + match.a['href']


                print(f'[INFO] Match {i}: ', teams, result_score, event_name, match_url)
                df = df.append({'date':date, 'team1':teams[0], 'team2':teams[1], 'result_score':result_score, 'event':event_name, 'match_url':match_url}, ignore_index=True)

    df.to_csv(f'result_parse_matches/result_parse_matches_{time()}.csv', sep=',', index=False)


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

def main():
    
    headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'content-type': 'text/html;charset=utf-8'
    }

    URL = r'https://www.hltv.org/results'

    response = requests.get(URL, headers=headers)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    result_matchs_count = int(soup.find(class_='pagination-data').text.split(' ')[-2])
    print('pagination: ', result_matchs_count)

    result_matchs_count = 100
    for i in range(result_matchs_count // 100):
        newURL = URL + f'?offset={i * 100}'

        
        response = requests.get(newURL, headers=headers)
        print('URL: ', newURL, 'status code: ', response.status_code)

        with open(f'./files/files_{i}.html', 'w') as f:
            f.write(response.text)
    

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        #Находим блок в сезультатами
        results_all = soup.find_all(class_='results-all')[-1]

        #Находим даты, в которых были матчи
        results_sublist = results_all.find_all(class_='results-sublist')

        with open(f'./files/files_match{1}.html', 'w') as f:
            f.write(str(results_sublist))
            
        #Находим матчи и саму дату
        for sublist in results_sublist:
            date = sublist.find(class_='standard-headline').text
            matches = sublist.find_all(class_='result-con')

            print('Date: ', date)
            print('Count matches: ', len(matches))

            #Находим названия матчей
            for i, match in enumerate(matches):
                teams = [team.text for team in match.find_all(class_='team')]
                event_name = match.find(class_='event-name').text
                result_score = match.find(class_='result-score').text
                match_url = 'hltv.org' + match.a['href']

                print(i, teams, result_score, event_name, match_url)


if __name__ == '__main__':
    #main()
    parse_matches(offset_stop=350, offset_start=150)
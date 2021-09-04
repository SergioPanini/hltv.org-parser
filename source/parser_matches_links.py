import requests
import bs4
import pandas as pd
from time import sleep, time
import random


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

def _get_pagination(URL: str, repeat_delay=1, max_delay = 10) -> int:
    '''Находит пагинацию(кол-во страниц)'''

    #Получаем все кол-во матчей
    try:
        response_text = _push_request(URL, repeat_delay=repeat_delay, max_delay=max_delay)
        soup = bs4.BeautifulSoup(response_text, 'html.parser')

        result_matchs_count = int(soup.find(class_='pagination-data').text.split(' ')[-2])
        return int(result_matchs_count)
    except:
        return None

def parse(repeat_delay=1, max_delay = 10, csv_file=None):
    '''Функция парсит матчи и сохраняет их в csv файл'''

    print('[INFO] _______Start Work_______')


    URL = r'https://www.hltv.org/results'

    #Создаем или открываем файл для записи данных
    if csv_file:
        df = pd.read_csv(csv_file, sep=',')
    
    else:
        df = pd.DataFrame(columns=['match_url'])
    
    print(df['match_url'])
    count_page = _get_pagination(URL, repeat_delay=1, max_delay = 10)
    if not count_page:
        print("[ERROR] Don't fing pagination")
        return 0
    
    print('[INFO] Pagination: ', count_page)

    for i in range((count_page // 100) + 1):
        newURL = URL + f'?offset={i * 100}'

        try:
            response_text = _push_request(newURL, repeat_delay=repeat_delay, max_delay=max_delay)

        except:
            print('[WARNING] Problems with url: ', newURL)
            continue

        soup = bs4.BeautifulSoup(response_text, 'html.parser')

        #Находим блок в сезультатами
        results_all = soup.find_all(class_='results-all')[-1]

        #Находим даты, в которых были матчи
        results_sublist = results_all.find_all(class_='results-sublist')
    
        #Находим матчи и саму дату
        for sublist in results_sublist:
            matches = sublist.find_all(class_='result-con')

            #Находим названия матчей
            for i, match in enumerate(matches):
                teams = [team.text for team in match.find_all(class_='team')]
                event_name = match.find(class_='event-name').text
                result_score = match.find(class_='result-score').text
                match_url = 'https://www.hltv.org' + match.a['href']

                
                print(f'[INFO] Match {i}: ', teams, result_score, event_name, match_url)
                
                #ПРоверяем что такой ссылки у нас нет и добавляем ее
                if not (True in list(df['match_url'] == match_url)):
                    df = df.append({'match_url':match_url}, ignore_index=True)

                #Иначе мы дошли до ссылки предыдущего парсинга и нужно останавливать парсинг
                else:
                    
                    df.to_csv('matches_links.csv', sep=',', index=False)
                    print('[INFO] _______END Work_______')  
                    
                    return

                        
    


if __name__ == '__main__':
    parse(csv_file='matches_links.csv')
    
from os import terminal_size
import requests, bs4

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
    main()
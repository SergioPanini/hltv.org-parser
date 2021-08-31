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
        URL += f'?offset={i * 100}'

        
        response = requests.get(URL, headers=headers)
        print('URL: ', URL, 'status code: ', response.status_code)

        with open(f'files_{i}.html', 'w') as f:
            f.write(response.text)
    

        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        all_results = soup.find_all(class_='results-all')[-1]
        result_matches = all_results.find_all(class_='results-sublist')
        
        for result in result_matches:
            data = result.find(class_='standard-headline')
            print('Data: ', data.text)

if __name__ == '__main__':
    main()
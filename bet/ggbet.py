import time
from typing import Dict, Optional, Tuple
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

from ggobjects import Match


class GGBet():
    '''Класс букмейкера на спорт'''


    def __init__(self):

        self.driver = webdriver.Firefox()

    def get_matchs_urls(self):
        '''Находим матчи на странице'''

        matchs_url = 'https://ggbet.ru/?sportIds[]=esports_counter_strike'
    
        self.driver.get(matchs_url)
        time.sleep(5)

        matchs_list = self.driver.find_elements(By.CLASS_NAME, 'sportEventRow__container___2gQB0')
        amount_matchs = len(matchs_list)
        N = -1
        
        while True:

            N += 1

            if N >= amount_matchs:
                
                #Загружаем новые матчи
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_matchs_list = self.driver.find_elements(By.CLASS_NAME, 'sportEventRow__container___2gQB0')
                new_amount_matchs = len(new_matchs_list)
                
                #Проверяем что новые матчи загрузились иначе они закончились
                if new_amount_matchs > amount_matchs:
                    amount_matchs = new_amount_matchs
                    matchs_list = new_matchs_list
                
                else:
                    break
            
            yield self.prepeare_match(matchs_list[N])
        
    @staticmethod
    def prepeare_match(match):
        '''Обработка верстки матча, вытаскиваем нужную информацию'''
        url = match.find_element(By.CLASS_NAME, '__app-LogoTitle-link').get_attribute('href')
        return url

    def get_ratio(self, url_match: str) -> Optional[Match]:
        '''Парсит коэфициенты на матч'''
        
        self.driver.execute_script(f"window.open('', '{url_match}');")
        match_handler = self.driver.window_handles[-1]
        self.driver.switch_to.window(match_handler)
        self.driver.get(url_match)

        try:
            ration = self.find_ratio(self.driver)
            teams = self.find_teams(self.driver)
            event_url = self.find_event_url(self.driver)

        except:
            return None

        match = Match(
            team1_name=teams[0],
            team2_name=teams[1],
            team1_ratio=ration[0],
            team2_ratio=ration[1],
            event_url=event_url,
            url=url_match,
            parse_datetime=str(datetime.datetime.now())
        )

        self.driver.close()

        return match
    
    @staticmethod
    def find_ratio(driver) -> Tuple[str]:
        '''Находит коэфициенты на странице'''
        
        ratio_container = driver.find_element(By.CLASS_NAME, '__app-PromoMatchOdds-container')
        left_team_ratio, right_team_ration = ratio_container.find_elements(By.CLASS_NAME, 'odd__ellipsis___3b4Yk')
        return left_team_ratio.text, right_team_ration.text
   
    @staticmethod
    def find_teams(driver) -> Tuple[str]:
        '''Парсит названия команд'''
        team1, team2 = driver.find_elements(By.CLASS_NAME, '__app-PromoMatchBody-competitor-name')
        return team1.text, team2.text
    
    @staticmethod
    def find_event_url(driver) -> str:
        '''Парсит ссылку на событие'''
        div = driver.find_element(By.CLASS_NAME, '__app-PromoMatchBody-tournament')
        a = div.find_element(By.TAG_NAME, 'a').text
        return a
    


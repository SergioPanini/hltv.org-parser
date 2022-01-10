import time
import datetime
from typing import Dict

from selenium import webdriver
from selenium.webdriver.common.by import By        

from objects import Match

class PariMatch:
    '''Класс букмейкера париматч'''

    def __init__(self):

        self.driver = webdriver.Firefox()

    def get_matchs_urls(self):
        '''Получаем список матчей'''

        matchs_url = 'https://www.parimatch.ru/ru/e-sports'
        match_class = '_2c98cYcZ15eCL3kXBibIh_'
    
        self.driver.get(matchs_url)
        time.sleep(3)

        matchs_list = self.driver.find_elements(By.CLASS_NAME, match_class)
        amount_matchs = len(matchs_list)
        N = -1
        
        while True:

            N += 1

            if N >= amount_matchs:
                
                #Загружаем новые матчи
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_matchs_list = self.driver.find_elements(By.CLASS_NAME, match_class)
                new_amount_matchs = len(new_matchs_list)
                
                #Проверяем что новые матчи загрузились иначе они закончились
                if new_amount_matchs > amount_matchs:
                    amount_matchs = new_amount_matchs
                    matchs_list = new_matchs_list
                
                else:
                    break
            
            yield self._get_url_by_match_webelement(matchs_list[N])
    
    @staticmethod
    def _get_url_by_match_webelement(match_webelement):
        '''Находит ссылку на матчи в элемента'''
        
        return match_webelement.find_element(By.TAG_NAME, 'a').get_attribute('href')

    def get_match_stats(self, url_match: str):
        '''Парсит коэфициенты на матч'''
        
        self.driver.execute_script(f"window.open('', '{url_match}');")
        match_handler = self.driver.window_handles[-1]
        self.driver.switch_to.window(match_handler)

        self.driver.get(url_match)
        time.sleep(5)
        ration = self.find_ratio(self.driver)
        match_time = self.driver.find_element(By.CLASS_NAME, '_Mj7yPrFfIXHcsQHA4_O0').text
        event = self.driver.find_element(By.CLASS_NAME, '_3j3p1F7S_rkp97PghYIpei').text
        team_left_name, team_right_name = self.driver.find_elements(By.CLASS_NAME, 'fJY3PlxtTVOlrlvGEv4UM')

        match = Match(
            event=event,
            team_left_name=team_left_name.text,
            team_right_name=team_right_name.text,
            team_left_ratio=ration[0],
            team_right_ratio=ration[1],
            url=url_match,
            match_time=match_time,
            parser_datetime=str(datetime.datetime.now())
        )

        self.driver.close()
        return match

    @staticmethod
    def find_ratio(driver) -> Dict[str, str]:
        '''Находит коэфициенты победы на странице'''

        pari = driver.find_elements(By.CLASS_NAME, '_3a3hikiZDvP_-_w8bGSiU7')
        pari = pari[0]
        
        rations = pari.find_elements(By.TAG_NAME, 'span')
        type_ration, team_1_ratio, team_2_ratio = rations 

        return team_1_ratio.text, team_2_ratio.text
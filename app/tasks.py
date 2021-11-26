from celery import Celery
from settings import BROKER
print(BROKER)
app = Celery(broker=BROKER)

app.conf.beat_schedule = {
    'check_new_match':
        {
            'task': 'check_new_match',
            'schedule': 3,
            'options': {'queue':'periodic_chech_queue'}
        },
    'check_new_bet':
        {
            'task': 'check_new_bet',
            'schedule': 3,
            'options': {'queue':'periodic_chech_queue'}
        }
}

@app.task
def check_new_match():
    '''Проверяет сайт на новые матчи'''

@app.task
def check_new_bet():
    '''Проверяет сайт на новые ставки'''

@app.task
def parse_new_match(url: str):
    '''Парсит новый матч'''

@app.task
def parse_new_bet(url: str):
    '''Парсит ставки'''
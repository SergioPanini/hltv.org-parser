import os

DB_USER = os.getenv('DB_USER', 'parser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 1234)
DB_NAME = os.getenv('DB_NAME', 'hltv')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', 5434)
DB = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

BROKER_USER = os.getenv('BROKER_USER') 
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')
BROKER_HOST = os.getenv('BROKER_HOST')
BROKER_PORT = os.getenv('BROKER_PORT') 
BROKER = f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}"
import os
import json
from random import randint

# DRIVER
DRIVER = '/usr/lib/chromium-browser/chromedriver'
# DRIVER = 'chromedriver'

# данные с config.json
json_config = json.load(open('config.json', 'r'))

# базовая задержка
SLEEP = int(json_config['SLEEP'])

# Текстовой запрос
TEXT_REQUEST = json_config['TEXT_REQUEST']

# # Ссылка для поиск - будет замена на текст внутри объявления
# LINK_SEARCH = json_config['LINK_SEARCH']
KEY_PHRASE = json_config['KEY_PHRASE']

# промежут сна для прокси
SLEEP_BEETWEEN_PROXY = (int(json_config['SLEEP_BEETWEEN_PROXY_FROM']), int(
    json_config['SLEEP_BEETWEEN_PROXY_TO']))

# сколько времени проводим на левом объявлении
TIME_AWAIT_OTHER_AD_FROM = SLEEP * 10
TIME_AWAIT_OTHER_AD_TO = SLEEP * 12

# сколько времени проводим на нужной странице
TIME_AWAIT_AD_FROM = SLEEP * 15
TIME_AWAIT_AD_TO = SLEEP * 20
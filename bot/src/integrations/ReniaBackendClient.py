import os
from typing import List
import requests
import json
from ..commands import BaseCommand, ManagedCommand
from requests.auth import HTTPBasicAuth
from ..bot.logs import logger

__url = 'http://renia-tg-backend:5001'
__username = os.environ.get('USR')
__password = os.environ.get('PASSWORD')
__auth = HTTPBasicAuth(__username, __password)

def __get(endpoint: str):
    return requests.get(f'{__url}{endpoint}', auth=__auth)


def get_commands() -> List[BaseCommand]:
    res = __get('/simple-commands')

    if res.status_code != 200:
        raise requests.RequestException(f'Backend odpowiedział kodem {res.status_code} ({res.reason})')

    commands = [ManagedCommand(**data) for data in json.loads(res.text)['result']]
    logger.info('Komendy zostały wczytane!')
    return commands


def should_enable_photo_command():
    return __get('/configs/photo_upload').status_code == 200


def get_simple_command_response(name):
    return __get(f'/simple-commands/{name}').text
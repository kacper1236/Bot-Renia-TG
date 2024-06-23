import os
from typing import List
import requests
import json
from ..commands import BaseCommand, ManagedCommand
from requests.auth import HTTPBasicAuth
from ..bot.logs import logger

URL = 'http://renia-tg-backend:5001'
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')


def get_commands() -> List[BaseCommand]:
    res = requests.get(f'{URL}/simple-commands',
                       auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if res.status_code != 200:
        raise requests.RequestException(f'Backend odpowiedział kodem {res.status_code} ({res.reason})')

    commands = [ManagedCommand(**data) for data in json.loads(res.text)['result']]
    logger.info('Komendy zostały wczytane!')
    return commands


def should_enable_photo_command():
    return requests.get(f'http://renia-tg-backend:5001/configs/photo_upload',
                        auth=HTTPBasicAuth(USERNAME, PASSWORD)).text


def get_simple_command_response(name):
    return requests.get(f'http://renia-tg-backend:5001/simple-commands/{name}',
                 auth=HTTPBasicAuth(USERNAME, PASSWORD)).text

def login_to_foxcons():
    a = requests.post("https://dev.foxcons.pl/app/auth/login/api", json={"loginToken": "your_token_here"})
    return a.text

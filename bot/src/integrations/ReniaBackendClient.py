import os
from typing import List
import requests
import json
from ..commands import BaseCommand, ManagedCommand
from requests.auth import HTTPBasicAuth
from ..bot.logs import logger

url = 'http://renia-tg-backend:5001'
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')


def get_simple_command_response(name):
    return requests.get(f'http://renia-tg-backend:5001/simple-commands/{name}',
                        auth=HTTPBasicAuth(ReniaBackendClient.USERNAME, ReniaBackendClient.PASSWORD)).text

class ReniaBackendClient:
    url = 'http://renia-tg-backend:5001'
    USERNAME = os.environ.get('USERNAME')
    PASSWORD = os.environ.get('PASSWORD')

    @staticmethod
    def get_commands() -> List[BaseCommand]:
        res = requests.get(f'{ReniaBackendClient.url}/simple-commands',
                           auth=HTTPBasicAuth(ReniaBackendClient.USERNAME, ReniaBackendClient.PASSWORD))
        
        if res.status_code != 200:
            raise requests.RequestException(f'Backend odpowiedział kodem {res.status_code} ({res.reason})')
        
        commands = [ManagedCommand(**data) for data in json.loads(res.text)['result']]

        logger.info('Komendy zostały wczytane!')

        return commands

    @staticmethod
    def should_enable_photo_command():
        return requests.get(f'http://renia-tg-backend:5001/configs/photo_upload',
                            auth=HTTPBasicAuth(ReniaBackendClient.USERNAME, ReniaBackendClient.PASSWORD)).text

    @staticmethod
    def get_simple_command_response(name):
        return requests.get(f'http://renia-tg-backend:5001/simple-commands/{name}',
                     auth=HTTPBasicAuth(ReniaBackendClient.USERNAME, ReniaBackendClient.PASSWORD)).text
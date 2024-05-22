
from typing import List
import requests
import json

from commands import BaseCommand, ManagedCommand
from logs import logger


class ReniaBackendClient:
    url = 'http://renia-tg-backend:5001'

    @staticmethod
    def get_commands() -> List[BaseCommand]:
        res = requests.get(f'{ReniaBackendClient.url}/simple-commands')

        if res.status_code != 200:
            raise requests.RequestException(f'Backend odpowiedział kodem {res.status_code} ({res.reason})')
        
        commands = [ManagedCommand(**data) for data in json.loads(res.text)['result']]

        logger.info('Komendy zostały wczytane!')

        return commands
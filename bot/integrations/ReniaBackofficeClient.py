
from typing import List
import requests
import json

from commands import BaseCommand, ManagedCommand
from logs import logger


class ReniaBackofficeClient:
    url = 'http://renia-tg-backend:5001'

    def get_commands(self) -> List[BaseCommand]:
        res = requests.get(f'{self.url}/configs')

        if res.status_code != 200:
            raise requests.RequestException(f'Backoffice odpowiedział kodem {res.status_code} ({res.reason})')
        
        commands = [ManagedCommand(**data) for data in json.loads(res.text)['result']]

        logger.info('Komendy zostały wczytane!')

        return commands
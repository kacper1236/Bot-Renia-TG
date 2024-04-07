from pyrogram import Client
from pathlib import Path
import os

class TesterClinet:

    @staticmethod
    def init(dir: Path) -> Client:
        '''
        Inicjalizacja klienta API Telegrama.
        '''
        return Client(
            'TesterClient',
            os.environ.get('TESTER_API_ID'),
            os.environ.get('TESTER_API_HASH'),
            workdir=dir
        )
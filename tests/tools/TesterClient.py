from pyrogram import Client
from dotenv import load_dotenv

import os

class TesterClinet:

    @staticmethod
    def init() -> Client:
        '''
        Inicjalizacja klienta API Telegrama.
        '''
        load_dotenv()
        return Client(
            'TesterClient',
            os.environ.get('TESTER_API_ID'),
            os.environ.get('TESTER_API_HASH')
        )
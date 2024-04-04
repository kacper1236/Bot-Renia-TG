
from abc import ABC, abstractmethod
from dataclasses import dataclass
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters
from logs import logger

def command_with_logs(func):
    '''Dekorator do logowania info'''
    async def wrapper(self, update: Update, context: CallbackContext):
        logger.info(f'Użytkownik {update.message.from_user.id} Wywołał komendę /{self.name}')
        await func(self, update, context)

    return wrapper

class BaseCommand(ABC):
    name: str
    '''Nazwa komendy, wykorzystywana do przypisania komendy'''
    description: str = None
    '''Krótki opis komendy do /help'''

    def get_handler_CommandHandler(self) -> CommandHandler:
        '''Komenda do przesyłania komendy do aplikacji

        Returns:
        CommandHandler: handler do komendy bota
        '''
        return CommandHandler(self.name, self.callback)
    
    def get_handler_MessageHandler(self) -> MessageHandler:
        '''Komenda do przesyłania komendy do aplikacji

        Returns:
        MessageHandler: handler do zdjęć i wideo + wiadomości
        '''
        return MessageHandler(filters.VIDEO | filters.PHOTO | filters.TEXT, self.callback)

    @abstractmethod
    async def callback(self, update: Update, context: CallbackContext):
        '''
        Funkcja obsługująca daną komendę

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass
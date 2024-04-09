from abc import ABC, abstractmethod
from dataclasses import dataclass
from telegram import Update
from telegram.ext import BaseHandler, CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler
from logs import logger
from typing import List, Dict

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

    @abstractmethod
    def get_handler(self) -> BaseHandler:
        '''Komenda do przesyłania komendy do aplikacji

        Returns:
        CommandHandler: handler do komendy bota
        '''
        pass

    @abstractmethod
    async def callback(self, update: Update, context: CallbackContext):
        '''
        Funkcja obsługująca daną komendę

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass

class SlashCommand(BaseCommand):
    def get_handler(self) -> BaseHandler:
        return CommandHandler(self.name, self.callback)

class MessageCommand(BaseCommand):
    filter : filters

    def get_handler(self) -> BaseHandler:
        return MessageHandler(self.filter, self.callback)
    
class ConversationCommand(BaseCommand):

    def get_handler(self) -> BaseHandler:
        return ConversationHandler(
            entry_points=[self.entry_points],
            states={state_name: [self.states] for state_name in self.state_names},
            fallbacks=[self.fallbacks]
        )

    @abstractmethod
    async def entry_points(self, update: Update, context: CallbackContext) -> List[BaseCommand]:
        '''
        Funkcja obsługująca wejście do konwersacji

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass

    @abstractmethod
    async def states(self, update: Update, context: CallbackContext) -> Dict[int, List[BaseCommand]]:
        '''
        Funkcja obsługująca stan konwersacji

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass
    
    @abstractmethod
    async def fallbacks(self, update: Update, context: CallbackContext) -> List[BaseCommand]:
        '''
        Funkcja obsługująca listę programów obsługi, które mogą zostać użyte w konwersacji

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass

 
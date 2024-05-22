from abc import ABC, abstractmethod
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
            entry_points=self.entry_points(),
            states={state: commands for state, commands in self.states().items()},
            fallbacks=self.fallbacks(),
            name = self.name,
            persistent=True
        )

    @abstractmethod
    def entry_points(self) -> List[BaseHandler]:
        '''
        Funkcja obsługująca wejście do konwersacji

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass

    @abstractmethod
    def states(self) -> Dict[int, List[BaseHandler]]:
        '''
        Funkcja obsługująca stan konwersacji

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass
    
    @abstractmethod
    def fallbacks(self) -> List[BaseHandler]:
        '''
        Funkcja obsługująca listę programów obsługi, które mogą zostać użyte w konwersacji

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass

 
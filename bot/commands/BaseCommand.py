
from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


class BaseCommand(ABC):
    name: str
    '''Nazwa komendy, wykorzystywana do przypisania komendy'''

    def get_handler(self) -> CommandHandler:
        '''Komenda do przesyłania komendy do aplikacji

        Returns:
        CommandHandler: handler do komendy bota
        '''
        return CommandHandler(self.name, self.callback)

    @abstractmethod
    async def callback(self, update: Update, context: CallbackContext):
        '''
        Funkcja obsługująca daną komendę

        Parameters:
        update: obiekt `Update`
        context: kontekst callbacku

        '''
        pass

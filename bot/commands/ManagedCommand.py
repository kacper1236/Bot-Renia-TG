from telegram import Update
from telegram.ext import CallbackContext
from . import BaseCommand

class ManagedCommand(BaseCommand):
    '''
    Komenda ustawiana poprzes UI Administratorskie
    '''
    
    def __init__(self, name: str, text: str) -> None:
        self.name = name
        self.text = text

    async def callback(self, update: Update, context: CallbackContext):
        await update.message.reply_text(self.text) 
            
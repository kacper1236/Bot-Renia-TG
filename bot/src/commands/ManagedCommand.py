from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs

class ManagedCommand(SlashCommand):
    '''
    Komenda ustawiana poprzes UI Administratorskie
    '''
    
    def __init__(self, name: str, text: str, description: str) -> None:
        self.name = name
        self.text = text
        self.description = description

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        await update.message.reply_text(self.text) 
            
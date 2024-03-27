
from telegram import Update
from telegram.ext import CallbackContext
from . import BaseCommand, command_with_logs
import requests


class HelpCommand(BaseCommand):
    name = 'help'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        await update.message.reply_text(f'Komendy: \n/ileDoFutrolajek\n/data\n/discord\n/strona')
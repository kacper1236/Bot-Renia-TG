
from telegram import Update
from telegram.ext import CallbackContext
from . import BaseCommand, command_with_logs
import requests


class HowMuchTimeToFutrolajkiCommand(BaseCommand):
    name = 'ileDoFutrolajek'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        resultFromConfig = requests.get("http://renia-tg-backend:5000/config/howMuchTimeToFutrolajki").text
        await update.message.reply_text(f'Zostalo: {resultFromConfig}')
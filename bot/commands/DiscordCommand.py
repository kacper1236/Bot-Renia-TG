
from telegram import Update
from telegram.ext import CallbackContext
from . import BaseCommand, command_with_logs
import requests


class DiscordCommand(BaseCommand):
    name = 'discord'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        resultFromConfig = requests.get("http://renia-tg-backend:5000/config/discord").text
        await update.message.reply_text(f'Oficjalny serwer Discord Futrołajek: {resultFromConfig}')
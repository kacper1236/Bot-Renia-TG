
from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs
import requests
import datetime

class HowMuchTimeLeftCommand(SlashCommand):
    name = 'ileDoFutrolajek'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        print("sssss")
        res = requests.get('https://futrolajki.pl/app/event/info')
        event_date = res.json()['eventDate']
        time_left = datetime.date.today() - event_date
        await update.message.reply_text(f'Do Futrołajek zostało {time_left}')
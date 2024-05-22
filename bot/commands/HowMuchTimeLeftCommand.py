from telegram import Update
from telegram.ext import CallbackContext
from . import command_with_logs, SlashCommand
import requests
import datetime


class HowMuchTimeLeftCommand(SlashCommand):
    name = 'ileDoFutrolajek'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        print("before request")
        event_date_str = requests.get('https://futrolajki.pl/app/event/info').json()['eventDate']
        event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%d").date()
        days_left = (event_date - datetime.date.today()).days
        await update.message.reply_text(f'Do Futrołajek zostało {days_left} dni')

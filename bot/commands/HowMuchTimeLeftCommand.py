from telegram import Update
from telegram.ext import CallbackContext
from . import command_with_logs, BaseCommand
import requests
import datetime


class HowMuchTimeLeftCommand(BaseCommand):
    name = 'ileDoFutrolajek'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        print("before request")
        res = requests.get('https://futrolajki.pl/app/event/info').json()
        print("after request")
        print(res)
        event_date = await res.json()['eventDate']
        print(event_date)
        time_left = datetime.date.today() - event_date
        await update.message.reply_text(f'Do Futrołajek zostało {time_left}')

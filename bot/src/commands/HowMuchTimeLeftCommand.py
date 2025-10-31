from telegram import Update
from telegram.ext import CallbackContext
from . import command_with_logs, SlashCommand
import requests
import datetime

class HowMuchTimeLeftCommand(SlashCommand):
    name = 'iledofutrolajek'
    description = 'Ile dni zostało do Futrołajek?'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        event_date_str = requests.get('https://futrolajki.pl/app/event/info').json()['eventDate']
        event_date = datetime.datetime.strptime(event_date_str, "%Y-%m-%d").date()
        days_left = (event_date - datetime.date.today()).days
        match days_left:
            case d if d <= -5:
                return await update.message.reply_text(f"Konwent już się zakończył :(")
            case d if d <= 0:
                return await update.message.reply_text(f"Konwent już się rozpoczął!")
            case 1:
                return await update.message.reply_text(f'Do Futrołajek został 1 dzień')
            case 2 | 3 | 4:
                return await update.message.reply_text(f'Do Futrołajek zostały {days_left} dni')
            case _:
                return await update.message.reply_text(f'Do Futrołajek zostało {days_left} dni')


from telegram import Update
from telegram.ext import CallbackContext
from . import BaseCommand

class TestCommand(BaseCommand):
    name = 'hello'

    async def callback(self, update: Update, context: CallbackContext):
        await update.message.reply_text(f'Hello {update.effective_user.first_name}')

from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs

class TestCommand(SlashCommand):
    name = 'hello'

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        await update.message.reply_text(f'Hello {update.effective_user.first_name}')
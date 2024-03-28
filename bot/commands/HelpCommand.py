
from telegram import Update
from telegram.ext import CallbackContext
from . import BaseCommand, command_with_logs, CommandManager

class HelpCommand(BaseCommand):
    name = 'help'

    def __init__(self, manager: CommandManager) -> None:
        super().__init__()
        self.__manager = manager

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        tokens = ['Komendy:']
        for command in self.__manager.handlers:
            tokens.append(f'/{command}')
        await update.message.reply_text('\n'.join(tokens))
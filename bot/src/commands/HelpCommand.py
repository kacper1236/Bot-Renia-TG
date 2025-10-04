from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs, CommandManager
from .translations import Translations
from .Database import Database
from ..bot.logs import logger

class HelpCommand(SlashCommand):
    translate = Translations()
    database = Database()

    name = 'help'
    description = 'commands'

    def __init__(self, manager: CommandManager) -> None:
        self.__manager = manager

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        try:
            language = self.database.select_one_piece('prefered_language', 'verified_users', f'id = {update.message.from_user.id}')
        except:
            language = None
        if language is None:
            language = 'pl'
        if language.lower() == "pl":
            tokens = ['Komendy:']
        else:
            tokens = ['Commands:']
        visible_commands = [command for command, is_visible in self.__manager.is_visible.items() if is_visible]
        for command, description in self.__manager.descriptions.items():
            if command not in visible_commands:
                continue
            command_line = [f'/{command}']
            if description is not None:
                command_line.append(self.translate.t(description, language))
            tokens.append(' - '.join(command_line))
        await update.message.reply_text('\n'.join(tokens))
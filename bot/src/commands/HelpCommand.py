
from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs, CommandManager

class HelpCommand(SlashCommand):
    name = 'help'
    description = 'pokaż wszystkie komendy'

    def __init__(self, manager: CommandManager) -> None:
        self.__manager = manager

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        tokens = ['Komendy:']
        for command, description in self.__manager.descriptions.items():
            command_line = [f'/{command}']
            if description is not None:
                command_line.append(description)
            tokens.append(' - '.join(command_line))
        await update.message.reply_text('\n'.join(tokens))
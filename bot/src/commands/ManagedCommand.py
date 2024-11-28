from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs
from ..bot.logs import logger
from ..integrations import ReniaBackendClient


class ManagedCommand(SlashCommand):
    '''
    Komenda ustawiana poprzes UI Administratorskie
    '''
    
    def __init__(self, name: str, text: str, description: str, is_visible:bool) -> None:
        self.name = name
        self.text = text
        self.description = description
        self.is_visible = is_visible

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        try:
            await update.message.reply_text(ReniaBackendClient.get_simple_command_response(self.name))
        except Exception:
            logger.exception("Renia napotkała błąd podczas pracy!")
            
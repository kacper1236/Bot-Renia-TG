from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, filters, ConversationHandler
from .BaseCommand import ConversationCommand
from . import command_with_logs
from .translations import Translations
import os
from ..bot.logs import logger

class Say(ConversationCommand):

    translate = Translations()

    name = "say"
    description = "say.help"
    is_visible = False

    SAVE = "SAY AS BOT"
    language = None

    filter = filters.TEXT | filters.Sticker.ALL | filters.VIDEO | filters.PHOTO

    async def start(self, update: Update, context: CallbackContext) -> int:
        if context.args and context.args[0] == os.environ.get("PASSWORD_FOR_COMMANDS"):
            try:
                self.language = self.database.select_one_piece('prefered_language', 'verified_users', f'id = {update.message.from_user.id}')
                await update.message.reply_text(self.translate.t("say.start"))
            except:
                await update.message.reply_text(self.translate.t("say.start", "pl"))
            return self.SAVE
        else:
            await update.message.reply_text(self.translate.t("say.wrong_password", "pl"))
            return ConversationHandler.END
    
    async def speak(self, update: Update, context: CallbackContext): 
        if update.message.text == "/end":
            return await self.end(update, context)
        try:
            await update.message.copy(chat_id = os.environ.get("CHANNEL_ID"), protect_content = True)
        except Exception as e:
            logger.info(e)

    async def end(self, update: Update, context: CallbackContext) -> int:
        try:
            await update.message.reply_text(self.translate.t("say.end", self.language))
        except Exception as e:
            await update.message.reply_text(self.translate.t("say.end", "pl"))
        return ConversationHandler.END

    def entry_points(self):
        return [CommandHandler(self.name, self.start)]

    def states(self):
        return {
            self.SAVE: [MessageHandler(self.filter, self.speak)]
        }
    
    def fallbacks(self):
        return [CommandHandler("end", self.end)]
    
    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        pass
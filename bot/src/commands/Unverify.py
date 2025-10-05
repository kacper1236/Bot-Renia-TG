from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
from . import ConversationCommand, command_with_logs
from ..bot.logs import logger
from .Database import Database
from .translations import Translations

class Unverify(ConversationCommand):

    database = Database()
    translate = Translations()
    UNVERIFY_STATE = "UNVERIFY_STATE"

    name = "unverify"
    description = "unverify.help"
    is_visible = False

    filter = filters.TEXT

    language = None

    async def start(self, update: Update, context: CallbackContext)-> int:
        logger.info(f"Użytkownik {update.message.from_user.id} wywołał komendę /unverify")
        try:
            self.language = self.database.select_one_piece('prefered_language', 'verified_users', f'id = {update.message.from_user.id}')
        except:
            await update.message.reply_text(self.translate.t("unverify.error", self.language))
            return ConversationHandler.END
        if self.database.select_one_piece('is_verified', 'verified_users', f'id = {update.message.from_user.id}') == False:
            await update.message.reply_text(self.translate.t("unverify.not_verify", self.language))
            return ConversationHandler.END
        await update.message.reply_text(self.translate.t("unverify.start", self.language))
        return self.UNVERIFY_STATE

    async def unverify_user(self, update: Update, context: CallbackContext):
        if update.message.text == "tak" or update.message.text == "yes":
            user_id = update.message.from_user.id
            self.database.update("verified_users", "is_verified", False, f"id = {user_id}")
            await update.message.reply_text(self.translate.t("unverify.end", self.language))
            return ConversationHandler.END
        else:
            return await self.stop(update, context)
    
    async def stop(self, update: Update, context: CallbackContext) -> int:
        if self.language is None:
            self.language = self.database.select_one_piece('prefered_language', 'verified_users', f'id = {update.message.from_user.id}')
        await update.message.reply_text(self.translate.t("unverify.cancel", self.language))
        return ConversationHandler.END

    def entry_points(self):
        return [CommandHandler(self.name, self.start)]

    def states(self):
        return {
            self.UNVERIFY_STATE: [MessageHandler(self.filter, self.unverify_user)]
        }
    
    def fallbacks(self):
        return [CommandHandler(self.name, self.stop)]

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        pass

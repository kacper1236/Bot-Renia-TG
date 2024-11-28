from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, filters, MessageHandler
from . import ConversationCommand, command_with_logs
import os
from ..bot.logs import logger
from .translations import Translations
from .Database import Database

from datetime import datetime

class UploadPhotoCommand(ConversationCommand):
    translate = Translations()
    database = Database()

    SAVE = "ZAPISZ_ZDJECIA"
    name = "upload"
    description = "upload photos.help"

    filter = filters.PHOTO | filters.VIDEO | filters.COMMAND | filters.TEXT

    language = None

    async def start(self, update: Update, context: CallbackContext) -> int:
        try:
            self.language = self.database.select_one_piece('prefered_language', 'verified_users', f'id = {update.message.from_user.id}')
            if self.database.select_one_piece('is_verified', 'verified_users', f'id = {update.message.from_user.id}') == False:
                await update.message.reply_text(self.translate.t("upload photos.not_verify", self.language))
                return ConversationHandler.END
        except:
            await update.message.reply_text("You are not verified user. Please use /verify command to verify yourself.")
            return ConversationHandler.END
        logger.info(f"Użytkownik {update.message.from_user.id} wywołał komendę /upload")
        await update.message.reply_text(self.translate.t("upload photos.start", self.language))
        return self.SAVE

    async def zapisz(self, update: Update, context: CallbackContext) -> int:
        try:
            user_id = update.message.from_user.id
            if update.message.effective_attachment.__class__ == tuple:
                logger.info(update.message.effective_attachment.__class__)
                file = update.message.effective_attachment[-1]
                logger.info(f"Użytkownik {user_id} wysłał zdjęcie o ID {file.file_id}")
                new_file = await file.get_file()
                await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"../photos/{user_id}_{datetime.now().timestamp()}.jpg"))
            else:
                new_file = await update.message.effective_attachment.get_file()
                await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"../photos/{user_id}_{datetime.now().timestamp()}.mp4"))
        except Exception as e:
            if update.message.text == "/end":
                return await self.end(update, context)
            logger.error(f"Podczas zapisywania zdjęcia wystąpił błąd: {e}")
            await update.message.reply_text(self.translate.t("upload photos.error", self.language))
    
    async def end(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text(self.translate.t("upload photos.end", self.language))
        return ConversationHandler.END

    def entry_points(self):
        return [CommandHandler(self.name, self.start)]

    def states(self):
        return {
            self.SAVE: [MessageHandler(self.filter, self.zapisz)]
        }
    
    def fallbacks(self):
        return [CommandHandler("end", self.end)]
    
    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        pass
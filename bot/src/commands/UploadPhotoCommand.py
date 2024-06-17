from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, filters, MessageHandler
from . import ConversationCommand, command_with_logs
import os
from ..bot.logs import logger

from datetime import datetime

class UploadPhotoCommand(ConversationCommand):
    SAVE = "ZAPISZ_ZDJECIA"
    name = "zdjecia"
    description = "Wyślij zdjęcia"

    filter = filters.PHOTO | filters.VIDEO | filters.COMMAND

    async def start(self, update: Update, context: CallbackContext) -> int:
        logger.info(f"Użytkownik {update.message.from_user.id} wywołał komendę /zapisz")
        await update.message.reply_text("Wyślij zdjęcie, które chcesz zapisać\n Aby zakończyć zapisywanie napisz /end")
        return self.SAVE

    async def zapisz(self, update: Update, context: CallbackContext) -> int:
        try:
            user_id = update.message.from_user.id
            file = update.message.effective_attachment[-1]
            logger.info(f"Użytkownik {user_id} wysłał zdjęcie o ID {file.file_id}")
            new_file = await file.get_file()
            await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"../photos/{user_id}_{datetime.now().timestamp()}.jpg"))
        except Exception as e:
            if update.message.text == "/end":
                return await self.end(update, context)
            logger.error(f"Podczas zapisywania zdjęcia wystąpił błąd: {e}")
            await update.message.reply_text("To nie jest zdjęcie, spróbuj ponownie\n Aby zakończyć zapisywanie napisz /end")
    
    async def end(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Zakończono zapisywanie zdjęć")
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
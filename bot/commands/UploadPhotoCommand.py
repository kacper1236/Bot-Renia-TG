from telegram import Update, Message
from telegram.ext import CallbackContext
from . import BaseCommand, command_with_logs, CommandManager

from datetime import datetime, timezone

class UploadPhotoCommand(BaseCommand):
    name = "zdjecia"
    description = "Wyślij zdjęcia"

    @command_with_logs
    async def callback(self, update: Update, context: Message):
        await update.message.reply_text("Siema")
        user_id = update.message.from_user.id
        timestamp = datetime.now().timestamp()
        new_file = await context.effective_attachment[-1].get_file()
        print(new_file)
        await new_file.download_to_drive(custom_path=f"C:\\Users\\kacpe\\Documents\\GitHub\\Bot-Renia-TG\\photos\\{user_id}_{timestamp}.jpg")
        await update.message.reply_text("Zdjęcie zostało zapisane")
from telegram import Update
from telegram.ext import CallbackContext
from . import MessageCommand, command_with_logs
import os

from datetime import datetime, timezone

class UploadPhotoCommand(MessageCommand):
    name = "zdjecia"
    description = "Wyślij zdjęcia"

    @command_with_logs
    async def callback(self, update:Update, context:CallbackContext):
        await update.message.reply_text("Rozpoczynam zapisywanie zdjęcia...")
        user_id = update.message.from_user.id
        timestamp = datetime.now().timestamp()
        new_file = await update.message.effective_attachment[-1].get_file()
        print(os.getcwd())
        print(os.listdir(".."))
        await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"../photos/{user_id}_{timestamp}.jpg"))
        await update.message.reply_text("Zdjęcie zostało zapisane")

        #Koniecznie do poprawy, bo bez użycia komendy sam pobiera zdjęcie, ALE POBIERA JE TAM GDZIE POWINNO BYĆ
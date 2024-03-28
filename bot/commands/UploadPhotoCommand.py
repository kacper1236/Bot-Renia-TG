from telegram import Update
from telegram.ext import CallbackContext
from . import BaseCommand, command_with_logs, CommandManager

class UploadPhotoCommand(BaseCommand):
    name = "zdjecia"
    description = "Wyślij zdjęcia"

    def __init__(self, manager: CommandManager) -> None:
        self.__manager = manager

    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        timestamp = update.message.date.strftime("%Y%m%d%H%M%S")
        file_id = update.message.photo[-1].file_id
        file_path = context.bot.get_file(file_id).file_path
        download_path = f"C:\\Users\\Rogal\\Documents\\GitHub\\Bot-Renia-TG\\photos\\{user_id}_{timestamp}.jpg"
        context.bot.download_file(file_path, download_path)
        await update.message.reply_text("Zdjęcie zostało zapisane")
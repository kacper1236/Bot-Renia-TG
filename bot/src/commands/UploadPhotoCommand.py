from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, filters
from . import ConversationCommand, command_with_logs, MessageCommand, SlashCommand
import os

from datetime import datetime

class UploadPhotoCommand(ConversationCommand):
    SAVE = range(1)
    name = "zdjecia"
    description = "Wyślij zdjęcia"
    state_names = [SAVE]
    miejsce_na_zdjecia = '/var/lib/photos'

    @command_with_logs
    async def start(self, update: Update, context: CallbackContext) -> int:
        print("start")
        await update.message.reply_text("Wyślij zdjęcie, które chcesz zapisać")
        return self.SAVE

    @command_with_logs
    async def save(self, update: Update, context: CallbackContext) -> int:
        print("save")
        await update.message.reply_text("Rozpoczynam zapisywanie zdjęcia...")
        user_id = update.message.from_user.id
        timestamp = datetime.now().timestamp()
        new_file = await update.message.effective_attachment[-1].get_file()
        print(os.getcwd())
        print(os.listdir(".."))
        await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"{miejsce_na_zdjecia}/{user_id}_{timestamp}.jpg"))
        await update.message.reply_text("Zdjęcie zostało zapisane")
        return ConversationHandler.END

    @command_with_logs
    async def entry_points(self, update: Update, context: CallbackContext):
        print("entry_points")
        return [SlashCommand("zdjecia", self.start)]
    
    @command_with_logs
    async def filter(self):
        return filters.PHOTO | filters.VIDEO & ~filters.COMMAND

    @command_with_logs
    async def states(self, update: Update, context: CallbackContext):
        print("states")
        return {
            self.SAVE: [MessageCommand(self.filter, self.save)]
        }
    
    @command_with_logs
    async def fallbacks(self, update: Update, context: CallbackContext):
        print("fallbacks")
        return []
    
    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        pass
    
    # @command_with_logs
    # async def callback(self, update:Update, context:CallbackContext):
    #     await update.message.reply_text("Rozpoczynam zapisywanie zdjęcia...")
    #     user_id = update.message.from_user.id
    #     timestamp = datetime.now().timestamp()
    #     new_file = await update.message.effective_attachment[-1].get_file()
    #     print(os.getcwd())
    #     print(os.listdir(".."))
    #     await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"{miejsce_na_zdjecia}/{user_id}_{timestamp}.jpg"))
    #     await update.message.reply_text("Zdjęcie zostało zapisane")

        #Koniecznie do poprawy, bo bez użycia komendy sam pobiera zdjęcie, ALE POBIERA JE TAM GDZIE POWINNO BYĆ

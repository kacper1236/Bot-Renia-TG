from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, filters, MessageHandler
from . import ConversationCommand, command_with_logs, MessageCommand, SlashCommand
import os

from datetime import datetime

class UploadPhotoCommand(ConversationCommand):
    SAVE = 1
    name = "zdjecia"
    description = "Wyślij zdjęcia"
    state_names = [SAVE]

    filter = filters.PHOTO | filters.VIDEO

    @command_with_logs
    async def start(self, update: Update, context: CallbackContext) -> int:
        print("start")
        await update.message.reply_text("Wyślij zdjęcie, które chcesz zapisać")
        return self.SAVE

    @command_with_logs
    async def save(self, update: Update, context: CallbackContext) -> int:
        try:
            print("save")
            await update.message.reply_text("Rozpoczynam zapisywanie zdjęcia...")
            user_id = update.message.from_user.id
            timestamp = datetime.now().timestamp()
            new_file = await update.message.effective_attachment[-1].get_file()
            await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"../photos/{user_id}_{timestamp}.jpg"))
            await update.message.reply_text("Zdjęcie zostało zapisane")
            return ConversationHandler.END
        except Exception as e:
            print(e)
            await update.message.reply_text("Wystąpił błąd podczas zapisywania zdjęcia")
            return ConversationHandler.END

    def entry_points(self):
        print("entry_points")
        return CommandHandler(self.name, self.start)

    def states(self):
        print("states")
        return {self.SAVE: [MessageHandler(self.filter, self.save)]}
    
    def fallbacks(self):
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
    #     await new_file.download_to_drive(custom_path=os.path.join(os.getcwd(), f"../photos/{user_id}_{timestamp}.jpg"))
    #     await update.message.reply_text("Zdjęcie zostało zapisane")

        #Koniecznie do poprawy, bo bez użycia komendy sam pobiera zdjęcie, ALE POBIERA JE TAM GDZIE POWINNO BYĆ
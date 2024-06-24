from telegram import Update
from telegram.ext import  CallbackContext, CommandHandler, ConversationHandler, filters, MessageHandler
from . import ConversationCommand, command_with_logs
from ..bot.logs import logger

class ConversationWithBot(ConversationCommand):
    coversation = "gadaniezbotem"

    name = "gadaniezbotem"
    description = "możesz gadać z botem"

    async def start(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Początek rozmowy z botem")
        return self.coversation
    
    async def conv(self, update: Update, context: CallbackContext) -> int:
        if update.message.text == "/end":
            return await self.end(update, context)
        await update.message.copy(update.message.chat_id, protect_content = True)
        return self.coversation
    
    async def end(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Koniec rozmowy z botem")
        return ConversationHandler.END
    
    def entry_points(self):
        return [CommandHandler(self.name, self.start)]
    
    def states(self):
        return {
            self.coversation: [MessageHandler(filters.ALL, self.conv)]
        }
    
    def fallbacks(self):
        return [CommandHandler("end", self.end)]
    
    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        pass

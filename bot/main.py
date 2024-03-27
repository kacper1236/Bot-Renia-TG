from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from dotenv import load_dotenv
import os
import sys

from commands import TestCommand

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def main():
    load_dotenv()
    
    app = ApplicationBuilder().token(os.environ['API_KEY']).build()
    command = TestCommand()
    app.add_handler(command.get_handler())

    app.run_polling()

if __name__ == "__main__":
    main()
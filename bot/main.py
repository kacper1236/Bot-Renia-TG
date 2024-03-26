from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
from dotenv import load_dotenv
import os

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def main():
    load_dotenv()
    
    app = ApplicationBuilder().token(os.environ['API_KEY']).build()

    app.add_handler(CommandHandler("hello", hello))

    app.run_polling()

if __name__ == "__main__":
    main()
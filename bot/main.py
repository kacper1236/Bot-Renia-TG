from pip._internal.commands.help import HelpCommand
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext
from dotenv import load_dotenv
import os
import sys

from commands.DateCommand import DateCommand
from commands.HowMuchTimeToFutrolajkiCommand import HowMuchTimeToFutrolajkiCommand
from commands.WebsiteCommand import WebsiteCommand
from commands.HelpCommand import HelpCommand
from commands.DiscordCommand import DiscordCommand
from commands import TestCommand
from logs import logger, error
import requests

def main():
    try:
        load_dotenv()
        app = ApplicationBuilder().token(os.environ.get('TG_TOKEN')).build()

        app.add_handler(TestCommand().get_handler())
        app.add_handler(HowMuchTimeToFutrolajkiCommand().get_handler())
        app.add_handler(WebsiteCommand().get_handler())
        app.add_handler(DiscordCommand().get_handler())
        app.add_handler(DateCommand().get_handler())
        app.add_handler(HelpCommand().get_handler())
        app.add_error_handler(error)

        logger.info("Renia jest włączona")
     
        app.run_polling() # wątek blokuje się na tym
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception:
        logger.exception("Renia napotkała błąd podczas pracy!")
    finally:
        logger.info("Renia konczy działanie")

if __name__ == "__main__":
    main()
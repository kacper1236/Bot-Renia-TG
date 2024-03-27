from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext
from dotenv import load_dotenv
import os
import sys

from commands import TestCommand
from logs import logger, error

def main():
    try:
        load_dotenv()

        app = ApplicationBuilder().token(os.environ['API_KEY']).build()

        app.add_handler(TestCommand().get_handler())
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
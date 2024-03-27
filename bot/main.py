from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
import os
import sys

from commands import TestCommand
from logs import logger

def main():
    try:
        load_dotenv()

        app = ApplicationBuilder().token(os.environ['API_KEY']).build()

        app.add_handler(TestCommand().get_handler())

        logger.info("Renia jest włączona")
     
        app.run_polling() # wątek blokuje się na tym

    except KeyboardInterrupt:
        pass
    except Exception as Argument:
        logger.exception("Renia napotkała błąd podczas pracy!")
        sys.exit(1)
    finally:
        logger.info("Renia konczy działanie")

if __name__ == "__main__":
    main()
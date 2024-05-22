from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
import os
import sys

from integrations import ReniaBackendClient
from commands import TestCommand, CommandManager, HelpCommand, UploadPhotoCommand, HowMuchTimeLeftCommand
from logs import logger, error

def main():
    try:
        load_dotenv()
        app = ApplicationBuilder().token(os.environ.get('TG_TOKEN')).build()

        manager = CommandManager(app)
        manager.setup([
            HelpCommand(manager),
            HowMuchTimeLeftCommand(),
            TestCommand(),
            UploadPhotoCommand(),
            *ReniaBackendClient.get_commands()
        ])

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
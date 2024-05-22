from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
import os
import sys

from integrations import ReniaBackendClient
from commands import TestCommand, CommandManager, HelpCommand, UploadPhotoCommand, HowMuchTimeLeftCommand, DatabasePersistence
from logs import logger, error
import requests

def main():
    try:
        load_dotenv()
        persistance = DatabasePersistence()
        app = ApplicationBuilder().token(os.environ.get('TG_TOKEN')).persistence(persistance).build()
        #app = ApplicationBuilder().token(os.environ.get('TG_TOKEN')).build()
        
        manager = CommandManager(app)
        availableCommands = [
            HelpCommand(manager),
            HowMuchTimeLeftCommand(),
            TestCommand(),
            *ReniaBackendClient.get_commands()
        ]
        enable_photo_command = requests.get(f'http://renia-tg-backend:5001/configs/photo_upload').text
        if enable_photo_command == '1':
            availableCommands.append(UploadPhotoCommand())

        manager.setup(availableCommands)
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
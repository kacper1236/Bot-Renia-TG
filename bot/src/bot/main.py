from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
import os
import sys
from ..integrations import ReniaBackendClient
from ..commands import CommandManager, HelpCommand, UploadPhotoCommand, HowMuchTimeLeftCommand, DatabasePersistence, Verify, Unverify, Say, Reload
from .logs import logger, error

persistence = DatabasePersistence()
app = ApplicationBuilder().token(os.environ.get('TG_TOKEN')).persistence(persistence).build()

manager = CommandManager(app)

static_commands = [
    HelpCommand(manager),
    HowMuchTimeLeftCommand(),
    Verify(),
    Unverify(),
    Say(),
    Reload(manager),
]

if ReniaBackendClient.should_enable_photo_command() == '1':
    static_commands.append(UploadPhotoCommand())

dynamic_commands = ReniaBackendClient.get_commands()

def main():
    global static_commands, dynamic_commands, app, manager
    try:
        load_dotenv()
        available_commands = [*static_commands, *dynamic_commands]

        manager.setup(available_commands)
        app.add_error_handler(error)
        logger.info("Renia jest włączona")
        app.run_polling()  # wątek blokuje się na tym
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception:
        logger.exception("Renia napotkała błąd podczas pracy!")
    finally:
        logger.info("Renia konczy działanie")


if __name__ == "__main__":
    main()
import logging.config
from telegram.error import NetworkError
from telegram import Update
from telegram.ext import CallbackContext
import traceback

# jak potrzebne będzie coś bardziej customowe
logging_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "simple": {
            "format": "|%(asctime)s|%(levelname)s:%(name)s| %(message)s",
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "filename": "../logs/renia.log",
            "encoding": "utf8"
        }
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["stdout", "file"]},
        "httpx": {"level": "WARNING", "handlers": ["stdout", "file"], "propagate": False},
        "httpcore": {"level": "WARNING", "handlers": ["stdout", "file"], "propagate": False},
        "telegram": {"level": "WARNING", "handlers": ["stdout", "file"], "propagate": False},
        "telegram.ext": {"level": "WARNING", "handlers": ["stdout", "file"], "propagate": False},
    }
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger('renia-bot')

async def error(update: Update, context: CallbackContext) -> None:
    """
    Handler obsługujący błędy.

    Parameters
    ----------
    update
        Obiekt `telegram.Update` posiadający informacje o requeście.
    context
        Obiekt `telegram.ext.CallbackContext`, który zawiera głównie podane argumenty.
    """
    if isinstance(context.error, (NetworkError)):
        logger.error(f'Błąd sieci: {context.error}')
    else:
        tb = traceback.format_exception(context.error)
        error_message = ''.join(tb)
        logger.error(f'Błąd: {error_message}')

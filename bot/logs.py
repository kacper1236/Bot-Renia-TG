import logging.config

from telegram import Update
from telegram.ext import CallbackContext


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
        "root": {"level": "DEBUG", "handlers": ["stdout", "file"]}
    }
}

logging.config.dictConfig(logging_config)

logger = logging.getLogger('renia-bot')

def error(update: Update, context: CallbackContext) -> None:
    """
    Handler obsługujący błędy.

    Parameters
    ----------
    update
        Obiekt `telegram.Update` posiadający informacje o requeście.
    context
        Obiekt `telegram.ext.CallbackContext`, który zawiera głównie podane argumenty.
    """

    logger.error(f'Renia napotkała błąd przy {update}: {context.error}')

import logging.config


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

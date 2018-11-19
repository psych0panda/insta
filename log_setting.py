import logging
import logging.config


def config_log(name):
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "console_log": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": "logs/debug.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "simple",
                "filename": "logs/errors.log",
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            }
        },

        "loggers": {
            "custom": {
                "level": "ERROR",
                "handlers": ["console", "info_file_handler", "error_file_handler"],
                "propagate": "no"
            }
        },

        "root": {
            "level": "DEBUG",
            "handlers": ["console", "info_file_handler", "error_file_handler"]
        }
    })
    return logging.getLogger(name)
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def logg():
    log_file = Path("shell.log")
    logger = logging.getLogger("shell")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt=' %Y-%m-%d %H:%M:%S')
    file_handler = RotatingFileHandler(str(log_file), maxBytes=1000000, backupCount=10, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

def log_command(logger, command, success=True, error_message=""):
    if success:
        logger.info(f"command: {command}")
    else:
        logger.error(f"in command{command} error: {error_message}")

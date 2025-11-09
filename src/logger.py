import logging
import datetime
from pathlib import Path

def logg():
    lod_file=Path("shell.log")
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s]%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(lod_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('shell.log')
def log_command(logger, command, success=True, error_message=""):
    if success:
        logger.info(command)
    else:
        logger.error(command)

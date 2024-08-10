import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Setup loggers
main_logger = setup_logger('main', 'logs/main.log')
scanner_logger = setup_logger('scanner', 'logs/scanner.log')

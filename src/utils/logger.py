# src/utils/logger.py

import logging
import os
from src.config.config import Config

def setup_logger(name):
    """
    Set up a logger with the specified name.

    :param name: The name of the logger.
    :return: The configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

    # Create file handler which logs even debug messages
    if not os.path.exists(os.path.dirname(Config.LOG_FILE)):
        os.makedirs(os.path.dirname(Config.LOG_FILE))
    fh = logging.FileHandler(Config.LOG_FILE)
    fh.setLevel(logging.DEBUG)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # Set the console logging level to DEBUG

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

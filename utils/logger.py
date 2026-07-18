"""Centralized logging setup for the retail sales analytics platform."""

import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def get_logger(name: str) -> logging.Logger:
    """Create and return a configured logger.

    Writes INFO and above to logs/app.log, and WARNING and above to the
    console, so normal operations stay in the log file while problems
    are still visible immediately.

    Args:
        name: Name for the logger, typically __name__ of the calling module.

    Returns:
        A configured logging.Logger instance.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.WARNING)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

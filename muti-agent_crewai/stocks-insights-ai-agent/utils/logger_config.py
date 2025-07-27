import logging
from logging.handlers import RotatingFileHandler
import os

# Define the log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Configure the logger
def setup_logger(name):
    """
    Set up a logger with a specific name.

    Args:
        name (str): Name of the logger (usually __name__ of the module).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Log everything, including debug-level messages

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Console logs only for info and above
    console_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_format)

    # File Handler (Rotating)
    log_file = os.path.join(LOG_DIR, f"{name}.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)

    # Add Handlers
    if not logger.hasHandlers():  # Avoid duplicate handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

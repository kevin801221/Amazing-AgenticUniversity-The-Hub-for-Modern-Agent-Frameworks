import logging
import os
import pytest
from utils.logger_config import setup_logger

# Test `setup_logger` function
def test_setup_logger_creates_logger():
    logger_name = "test_logger"
    logger = setup_logger(logger_name)

    # Verify logger is created
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name

def test_logger_has_console_handler():
    logger_name = "test_logger"
    logger = setup_logger(logger_name)

    # Check for console handler
    console_handlers = [
        handler for handler in logger.handlers if isinstance(handler, logging.StreamHandler)
    ]
    assert len(console_handlers) == 1

    console_handler = console_handlers[0]
    assert console_handler.level == logging.INFO

def test_logger_has_file_handler():
    logger_name = "test_logger"
    logger = setup_logger(logger_name)

    # Check for file handler
    file_handlers = [
        handler for handler in logger.handlers if isinstance(handler, logging.handlers.RotatingFileHandler)
    ]
    assert len(file_handlers) == 1

    file_handler = file_handlers[0]
    assert file_handler.level == logging.DEBUG

def test_file_logging_creates_log_file():
    logger_name = "test_logger_file"
    log_dir = "logs"
    logger = setup_logger(logger_name)

    # Write a debug log
    logger.debug("This is a debug message")

    # Verify log file is created
    log_file_path = os.path.join(log_dir, f"{logger_name}.log")
    assert os.path.exists(log_file_path)

    # Verify log content
    with open(log_file_path, "r") as log_file:
        log_content = log_file.read()
        assert "This is a debug message" in log_content

def test_log_rotation():
    logger_name = "test_logger_rotation"
    log_dir = "logs"
    logger = setup_logger(logger_name)

    # Simulate log rotation by writing large logs
    log_file_path = os.path.join(log_dir, f"{logger_name}.log")
    for _ in range(10000):  # Create a large log to exceed 5MB
        logger.debug("This is a test message for rotation")

    # Check if multiple log files are created
    rotated_files = [
        file for file in os.listdir(log_dir) if file.startswith(logger_name)
    ]
    assert len(rotated_files) > 1  # At least one rotated file should exist

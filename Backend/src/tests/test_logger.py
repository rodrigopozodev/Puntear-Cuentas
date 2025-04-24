import logging
import pytest
from src.utils.logger import setup_logger

@pytest.fixture
def logger():
    setup_logger()
    logger = logging.getLogger()
    return logger

def test_logger_setup(logger):
    assert logger is not None
    assert isinstance(logger, logging.Logger)

def test_logger_info(logger, caplog):
    with caplog.at_level(logging.INFO):
        logger.info("Test info message")
    assert "Test info message" in caplog.text

def test_logger_error(logger, caplog):
    with caplog.at_level(logging.ERROR):
        logger.error("Test error message")
    assert "Test error message" in caplog.text

def test_logger_warning(logger, caplog):
    with caplog.at_level(logging.WARNING):
        logger.warning("Test warning message")
    assert "Test warning message" in caplog.text
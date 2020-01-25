import pytest
import logging_setup
import logging


def test_logging_setup():
    logger = logging_setup.get_logger("api_flow")
    assert logger.name == "api_flow"
    assert logger.level == logging.DEBUG
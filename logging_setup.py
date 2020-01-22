import logging.config
import logging
import yaml


def get_logger(logger_name):
    """

    :type logger_name: str
    :rtype: logging.Logger
    """
    with open('logging.yaml', 'r') as f:
        log_cfg = yaml.safe_load(f.read())

    logging.config.dictConfig(log_cfg)
    return logging.getLogger(logger_name)

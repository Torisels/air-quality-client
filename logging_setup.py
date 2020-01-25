import logging.config
import logging
import yaml
import helpers

CONF_FILE_NAME = "logging.yaml"


def get_logger(logger_name):
    """
    Returns logger with specified name. Uses logging.yaml as logging configuration.

    :type logger_name: str
    :rtype: logging.Logger
    """

    path_to_file = helpers.relative_path(CONF_FILE_NAME)
    with open(path_to_file, 'r') as f:
        log_cfg = yaml.safe_load(f.read())

    logging.config.dictConfig(log_cfg)
    return logging.getLogger(logger_name)

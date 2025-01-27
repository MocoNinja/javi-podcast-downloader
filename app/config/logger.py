import logging

from app.config import config

_ROOT_LOGGER_NAME = "SCRAPPER_LOGGER"
ROOT_LOGGER = None


def _init_root_logger():
    global ROOT_LOGGER
    if ROOT_LOGGER is not None:
        ROOT_LOGGER.debug("Logger is already initialized. Pass...")
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(_ROOT_LOGGER_NAME)
    logger.setLevel(config.LOG_LEVEL)
    logger.propagate = False

    if not logger.hasHandlers():
        logger.addHandler(handler)

    ROOT_LOGGER = logger


_init_root_logger()

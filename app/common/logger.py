import logging

"""
    Custom logger for the application.
"""

_ROOT_LOGGER_NAME: str = "SCRAPPER_LOGGER"
_ROOT_LOGGER: logging.Logger | None = None


def is_enabled_for_level(level) -> bool:
    """
    Expose root logger method to check if given level is enabled
    :param level: the level to check
    :return:  if enabled
    """
    return _ROOT_LOGGER.isEnabledFor(level)


def log(level, msg) -> None:
    """
    Expose root logger method to log a msg at a level
    :param level:  the level to log in
    :param msg: the msg to log
    """
    _ROOT_LOGGER.log(level, msg)


def info(msg) -> None:
    """
    Expose root logger method to log a msg at level info
    :param msg:  the msg to log
    """
    _ROOT_LOGGER.info(msg)


def warning(msg) -> None:
    """
    Expose root logger method to log a msg at level warning
    :param msg:  the msg to log
    """
    _ROOT_LOGGER.warning(msg)


def error(msg) -> None:
    """
    Expose root logger method to log a msg at level error
    :param msg:  the msg to log
    """
    _ROOT_LOGGER.error(msg)


def fatal(msg) -> None:
    """
    Expose root logger method to log a msg at level fatal
    :param msg:  the msg to log
    """
    _ROOT_LOGGER.fatal(msg)


def debug(msg) -> None:
    """
    Expose root logger method to log a msg at level debug
    :param msg:  the msg to log
    """
    _ROOT_LOGGER.debug(msg)


def init_root_logger(level) -> None:
    """
    Configure the logging for the application.
    """
    global _ROOT_LOGGER
    if _ROOT_LOGGER is not None:
        _ROOT_LOGGER.debug("Logger is already initialized. Pass...")
        return

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(_ROOT_LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.hasHandlers():
        logger.addHandler(handler)

    _ROOT_LOGGER = logger

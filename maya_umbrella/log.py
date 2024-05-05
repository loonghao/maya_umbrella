# Import built-in modules
import logging.handlers
import os

# Import local modules
from maya_umbrella.constants import LOG_FORMAT
from maya_umbrella.constants import LOG_MAX_BYTES
from maya_umbrella.constants import PACKAGE_NAME
from maya_umbrella.filesystem import get_log_file


def setup_logger(logger=None, logfile=None, log_level=None):
    """Set up the logger with the specified log file and log level.

    Args:
        logger (logging.Logger, optional): The logger to set up. Defaults to the logger for the package.
        logfile (str, optional): The path to the log file. Defaults to the log file returned by `get_log_file()`.
        log_level (int, optional): The log level. Defaults to `logging.INFO`.

    Returns:
        logging.Logger: The set up logger.
    """
    logger = logger or logging.getLogger(PACKAGE_NAME)
    log_level = log_level or os.getenv("MAYA_UMBRELLA_LOG_LEVEL", "INFO")
    logger.setLevel(log_level)
    logfile = logfile or get_log_file()
    if not len(logger.handlers):
        filehandler = logging.handlers.RotatingFileHandler(
            logfile,
            mode="a",
            backupCount=7,
            delay=True,
            maxBytes=LOG_MAX_BYTES,
        )
        filehandler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(filehandler)
    return logger

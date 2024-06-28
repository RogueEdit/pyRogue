# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Author
# Date of release: 06.06.2024
# Last Edited: 28.06.2024

"""
This script provides a custom logger that logs messages to a weekly rotating log file. It includes functionality to
exclude specific log messages and to temporarily deactivate and reactivate logging.

Features:
- Weekly rotating log file creation.
- Custom log message filtering.
- Temporary deactivation and reactivation of logging.

Modules:
- logging: Python's built-in logging module.
- os: Module for interacting with the operating system.
- logging.handlers: Module for logging handler classes.
- datetime: Module for manipulating dates and times.

Workflow:
1. Initialize the custom logger with a weekly rotating file handler.
2. Provide methods to deactivate and reactivate logging.
"""
from modules import config

import logging
# Provides logging capabilities for creating log messages and managing log levels.

import os
# Provides a way to interact with the operating system, particularly for file and directory operations.

from logging.handlers import TimedRotatingFileHandler
# Provides a logging handler that rotates log files at specified intervals (e.g., weekly).

from datetime import datetime
# Provides date and time manipulation capabilities, particularly for timestamping log files.

class CustomFilter(logging.Filter):
    """
    Custom filter to exclude log messages containing specific text.

    :param record: The log record to filter.
    :type record: logging.LogRecord
    :return: Whether the log record should be included.
    :rtype: bool
    """
    def filter(self, record):
        return "data={\"value\":" not in record.getMessage()

class CustomLogger:
    """
    A custom logger class that logs messages to a weekly log file.

    This logger initializes a TimedRotatingFileHandler that creates a new log file
    every week. It also includes a custom filter to exclude specific log messages.

    :arguments:
    None

    :params:
    None

    Usage:
        Initialize the custom logger in your script to start logging:
        >>> logger = CustomLogger()

        Temporarily deactivate logging:
        >>> CustomLogger.deactivate_logging()

        Reactivate logging:
        >>> CustomLogger.reactivate_logging()

    Output examples:
        - Log file created at logs/YYYY-WW.log with formatted log messages.
        - Log messages filtered based on custom criteria.

    Modules:
        - logging: Provides logging capabilities for creating log messages and managing log levels.
        - os: Interacts with the operating system for file and directory operations.
        - logging.handlers: Provides a handler that rotates log files at specified intervals.
        - datetime: Manipulates dates and times for timestamping log files.
    """
    def __init__(self):
        # Create and configure file handler
        # Define the path to the logs directory in the current working directory
        logsDirectory = config.logsDirectory

        formatterFile = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create file handler and set level to DEBUG for file output
        logFilename = os.path.join(logsDirectory, f'{datetime.now().strftime("%Y-%W")}.log')
        fh = TimedRotatingFileHandler(logFilename, when='W0', backupCount=52)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatterFile)

        # Add custom filter to file handler
        fh.addFilter(CustomFilter())

        # Add file handler to the root logger
        rootLogger = logging.getLogger()
        rootLogger.propagate = False
        rootLogger.setLevel(logging.DEBUG)  # Ensure root logger level is set to DEBUG
        if not any(isinstance(handler, TimedRotatingFileHandler) for handler in rootLogger.handlers):
            rootLogger.addHandler(fh)

        # Remove default console handler to avoid outputs since we want to display them colored with less information
        for handler in rootLogger.handlers:
            if isinstance(handler, logging.StreamHandler):
                rootLogger.removeHandler(handler)

    @staticmethod
    def fh_deactiveLogging():
        """
        Temporarily deactivate logging.

        This method sets the logging level of TimedRotatingFileHandler to NOTSET,
        effectively silencing logging output temporarily.

        :arguments:
        None

        :params:
        None

        Usage:
            Temporarily deactivate logging:
            >>> CustomLogger.deactivate_logging()
        """
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, TimedRotatingFileHandler):
                handler.setLevel(logging.NOTSET)

    @staticmethod
    def fh_reactiveLogging():
        """
        Reactivate logging.

        This method sets the logging level of TimedRotatingFileHandler back to DEBUG,
        re-enabling logging output.

        :arguments:
        None

        :params:
        None

        Usage:
            Reactivate logging:
            >>> CustomLogger.reactivate_logging()
        """
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, TimedRotatingFileHandler):
                handler.setLevel(logging.DEBUG)

if __name__ == '__main__':
    logger = CustomLogger()

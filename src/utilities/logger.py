# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 06.06.2024 
# Last Edited. 20.06.2024

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Define the path to the logs directory in the current working directory
logs_directory = os.path.join(os.getcwd(), 'logs')

# Create the logs directory if it doesn't exist
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
    print(f'Created logs directory: {logs_directory}')

class CustomFilter(logging.Filter):
    def filter(self, record):
        """
        Exclude log messages containing specific text.

        :param record: The log record to filter.
        :type record: logging.LogRecord
        :return: Whether the log record should be included.
        :rtype: bool
        """
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
        - logging: Python's built-in logging module.
        - os: Module for interacting with the operating system.
        - logging.handlers: Module for logging handler classes.
        - datetime: Module for manipulating dates and times.
    """
    def __init__(self):
        # Create and configure file handler
        formatter_file = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create file handler and set level to DEBUG for file output
        log_filename = os.path.join(logs_directory, f'{datetime.now().strftime("%Y-%W")}.log')
        fh = TimedRotatingFileHandler(log_filename, when='W0', backupCount=52)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter_file)

        # Add custom filter to file handler
        fh.addFilter(CustomFilter())

        # Add file handler to the root logger
        root_logger = logging.getLogger()
        root_logger.propagate = False
        root_logger.setLevel(logging.DEBUG)  # Ensure root logger level is set to DEBUG
        if not any(isinstance(handler, TimedRotatingFileHandler) for handler in root_logger.handlers):
            root_logger.addHandler(fh)

        # Remove default console handler to avoid outputs since we want to display them colored with less information
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                root_logger.removeHandler(handler)
    
    @staticmethod
    def deactivate_logging():
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
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            if isinstance(handler, TimedRotatingFileHandler):
                handler.setLevel(logging.NOTSET)

    @staticmethod
    def reactivate_logging():
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
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            if isinstance(handler, TimedRotatingFileHandler):
                handler.setLevel(logging.DEBUG)

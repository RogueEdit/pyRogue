# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 06.06.2024 

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
        # Exclude log messages containing "data={"value":"
        return "data={\"value\":" not in record.getMessage()

class CustomLogger:
    """
    A custom logger class that logs messages to a weekly log file.
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

        # Remove default console handler to avoid outputs since we want to display em colored with less information
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                root_logger.removeHandler(handler)
    
    @staticmethod
    def deactivate_logging():
        """
        Temporarily deactivate logging.
        """
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            if isinstance(handler, TimedRotatingFileHandler):
                handler.setLevel(logging.NOTSET)

    @staticmethod
    def reactivate_logging():
        """
        Reactivate logging.
        """
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            if isinstance(handler, TimedRotatingFileHandler):
                handler.setLevel(logging.DEBUG)
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from utilities.cFormatter import cFormatter

# Define the path to the logs directory in the current working directory
logs_directory = os.path.join(os.getcwd(), 'logs')

# Create the logs directory if it doesn't exist
if not os.path.exists(logs_directory):
    os.makedirs(logs_directory)
    print(f"Created logs directory: {logs_directory}")

class CustomLogger:
    """
    A custom logger class that logs messages to the console with color formatting and to a weekly log file.
    """

    def __init__(self):
        # Create and configure logger for console
        self.logger_console = logging.getLogger('console')
        self.logger_console.setLevel(logging.DEBUG)

        # Create color formatter for console output
        formatter_console = cFormatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create color handler and set level to DEBUG for console output
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter_console)

        # Add console handler to console logger
        self.logger_console.addHandler(ch)

        # Create and configure file handler
        formatter_file = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Create file handler and set level to DEBUG for file output
        log_filename = os.path.join(logs_directory, f"{datetime.now().strftime('%Y-%W')}.log")
        fh = TimedRotatingFileHandler(log_filename, when='W0', backupCount=52)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter_file)

        # Add file handler to console logger
        self.logger_console.addHandler(fh)  # Add file handler to console logger

        # Add file handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(fh)
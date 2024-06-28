# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Author
# Date of release: 06.06.2024
# Last Edited: 28.06.2024

"""
This script provides a lockout mechanism to limit the frequency of function executions. It includes functionality to
persistently store the last execution timestamps of functions and prevent re-execution within a specified lockout period.

Features:
- Limit function execution frequency with a lockout period.
- Persistent storage of execution timestamps.
- Colored output for log messages.

Modules:
- os: Module for interacting with the operating system.
- json: Module for working with JSON data.
- time: Module for time-related functions.
- functools: Module for higher-order functions.
- utilities.cFormatter: Custom formatter for colored printing and logging.

Workflow:
1. Initialize the Limiter class with a lockout period and optional timestamp file path.
2. Decorate functions with the lockout decorator to enforce execution limits.
3. Use the decorated functions as usual, with lockout limits applied.
"""

import os
# Provides a way to interact with the operating system, particularly for file and directory operations.

import json
# Provides functionalities to work with JSON data for reading and writing timestamps.

import time
# Provides time-related functions, particularly for getting the current time.

from functools import wraps
# Provides utilities for higher-order functions, particularly for creating decorators.

from utilities import cFormatter, Color
# Custom module for colored printing and logging functionalities.

from modules.config import timestampFile

class Limiter:
    """
    A class to handle lockout mechanism for functions to limit their execution frequency.

    Attributes:
        lockout_period (int): The lockout period in seconds.
        timestamp_file (str): The file path to store the timestamps.

    :arguments:
    - lockout_period (int): The lockout period in seconds.

    :params:
    None

    Usage:
        Initialize the limiter and decorate functions to limit their execution frequency:
        >>> limiter = Limiter(lockout_period=60)
        >>> @limiter.lockout
        >>> def my_function():
        >>>     print("Function executed.")

    Output examples:
        - Prints a message if the function is called within the lockout period.
        - Executes the function and updates the timestamp if called outside the lockout period.

    Modules:
        - os: Module for interacting with the operating system.
        - json: Module for working with JSON data.
        - time: Module for time-related functions.
        - functools: Module for higher-order functions.
        - utilities.cFormatter: Custom formatter for colored printing and logging.
    """
    
    def __init__(self, lockoutPeriod: int = 40):
        """
        Initialize the Limiter object.

        Args:
            lockout_period (int): The lockout period in seconds.
            timestamp_file (str, optional): The file path to store the timestamps. Default is './data/extra.json'.

        Modules:
            - os: Provides a way to interact with the operating system, particularly for file and directory operations.
            - json: Provides functionalities to work with JSON data for reading and writing timestamps.
        """
        
        self.lockoutPeriod = lockoutPeriod
        self.timestampFile = timestampFile
        if not os.path.exists(os.path.dirname(self.timestampFile)):
            os.makedirs(os.path.dirname(self.timestampFile))
        if not os.path.exists(self.timestampFile):
            with open(self.timestampFile, 'w') as f:
                json.dump({}, f)

    def lockout(self, func):
        """
        Decorator function to enforce the lockout mechanism on the decorated function.

        Args:
            func (function): The function to be decorated.

        Returns:
            function: The decorated function.

        Usage:
            Decorate a function with the lockout decorator to limit its execution frequency:
            >>> limiter = Limiter(lockout_period=60)
            >>> @limiter.lockout
            >>> def my_function():
            >>>     print("Function executed.")

        Modules:
            - functools: Provides utilities for higher-order functions, particularly for creating decorators.
            - time: Provides time-related functions, particularly for getting the current time.
            - utilities.cFormatter: Custom formatter for colored printing and logging.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            funcName = func.__name__
            laxtExecTime = self._fh_getLastExecTime(funcName)
            currentTime = time.time()
            if currentTime - laxtExecTime < self.lockoutPeriod:
                cFormatter.print(Color.RED, f'{funcName} is rate limited. You can only do this every {self.lockoutPeriod} seconds!', isLogging=True)
                return None
            else:
                result = func(*args, **kwargs)
                self._fh_updateLastExecTime(funcName, currentTime)
                return result
        return wrapper

    def _fh_getLastExecTime(self, func_name: str) -> float:
        """
        Get the timestamp of the last execution of a function.

        Args:
            func_name (str): The name of the function.

        Returns:
            float: The timestamp of the last execution.

        Usage:
            Get the last execution time of a function:
            >>> last_exec_time = limiter._get_last_exec_time('my_function')

        Modules:
            - json: Provides functionalities to work with JSON data for reading and writing timestamps.
        """
        with open(self.timestampFile, 'r') as f:
            timestamps = json.load(f)
        return timestamps.get(func_name, 0)

    def _fh_updateLastExecTime(self, func_name: str, timestamp: float) -> None:
        """
        Update the timestamp of the last execution of a function.

        Args:
            func_name (str): The name of the function.
            timestamp (float): The timestamp of the last execution.

        Usage:
            Update the last execution time of a function:
            >>> limiter._update_last_exec_time('my_function', time.time())

        Modules:
            - json: Provides functionalities to work with JSON data for reading and writing timestamps.
        """
        with open(self.timestampFile, 'r+') as f:
            try:
                timestamps = json.load(f)
            except json.decoder.JSONDecodeError:
                timestamps = {}
            timestamps[func_name] = timestamp
            f.seek(0)
            json.dump(timestamps, f, indent=4)
            f.truncate()

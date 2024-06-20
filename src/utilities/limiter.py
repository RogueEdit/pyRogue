# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 06.06.2024
# Last Edited: 20.06.2024

import os
import json
import time
from functools import wraps
from utilities.cFormatter import cFormatter, Color

class Limiter:
    """
    A class to handle lockout mechanism for functions to limit their execution frequency.

    Attributes:
        lockout_period (int): The lockout period in seconds.
        timestamp_file (str): The file path to store the timestamps.

    :arguments:
    - lockout_period (int): The lockout period in seconds.
    - timestamp_file (str, optional): The file path to store the timestamps. Default is './data/extra.json'.

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
    
    def __init__(self, lockout_period: int, timestamp_file: str = './data/extra.json'):
        self.lockout_period = lockout_period
        self.timestamp_file = timestamp_file
        if not os.path.exists(os.path.dirname(self.timestamp_file)):
            os.makedirs(os.path.dirname(self.timestamp_file))
        if not os.path.exists(self.timestamp_file):
            with open(self.timestamp_file, 'w') as f:
                json.dump({}, f)

    def lockout(self, func):
        """
        Decorator function to enforce the lockout mechanism on the decorated function.

        :arguments:
        - func (function): The function to be decorated.

        :params:
        None

        Returns:
            function: The decorated function.

        Usage:
            Decorate a function with the lockout decorator to limit its execution frequency:
            >>> limiter = Limiter(lockout_period=60)
            >>> @limiter.lockout
            >>> def my_function():
            >>>     print("Function executed.")
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            last_exec_time = self._get_last_exec_time(func_name)
            current_time = time.time()
            if current_time - last_exec_time < self.lockout_period:
                cFormatter.print(Color.RED, f'{func_name} is rate limited. You can only do this every {self.lockout_period} seconds!', isLogging=True)
                return None
            else:
                result = func(*args, **kwargs)
                self._update_last_exec_time(func_name, current_time)
                return result
        return wrapper

    def _get_last_exec_time(self, func_name: str) -> float:
        """
        Get the timestamp of the last execution of a function.

        :arguments:
        - func_name (str): The name of the function.

        :params:
        None

        Returns:
            float: The timestamp of the last execution.

        Usage:
            Get the last execution time of a function:
            >>> last_exec_time = limiter._get_last_exec_time('my_function')
        """
        with open(self.timestamp_file, 'r') as f:
            timestamps = json.load(f)
        return timestamps.get(func_name, 0)

    def _update_last_exec_time(self, func_name: str, timestamp: float) -> None:
        """
        Update the timestamp of the last execution of a function.

        :arguments:
        - func_name (str): The name of the function.
        - timestamp (float): The timestamp of the last execution.

        :params:
        None

        Usage:
            Update the last execution time of a function:
            >>> limiter._update_last_exec_time('my_function', time.time())
        """
        with open(self.timestamp_file, 'r+') as f:
            try:
                timestamps = json.load(f)
            except json.decoder.JSONDecodeError:
                timestamps = {}
            timestamps[func_name] = timestamp
            f.seek(0)
            json.dump(timestamps, f, indent=4)
            f.truncate()

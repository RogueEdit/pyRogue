# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 13.06.2024 
# Last Edited: 25.06.2024
# Based on: https://github.com/pagefaultgames/pokerogue/

"""
This script provides a class 'Rogue' for interacting with the PokeRogue API to manage trainer and gamesave data.

Functionality:
- Fetches and updates trainer data and gamesave slots from the PokeRogue API.
- Handles data dumping to local files and creates backups.
- Implements HTTP requests and Selenium WebDriver for API interactions.

Modules:
- json: Provides support for parsing JSON data.
- random: Generates random numbers, used for various utilities.
- os: Provides functions for interacting with the operating system, used for file operations.
- shutil: Offers high-level operations on files and directories, used for file management.
- brotli: Compression library (unused in this script).
- time: Provides time-related functions, used for timing operations.
- typing: Supports type hints for Python code.
- logging: Offers logging capabilities for tracking events and errors.
- colorama.Style: Part of colorama library for terminal text styling.
- re: Provides support for regular expressions, used for text matching.
- datetime: Supports date and time manipulation.
- requests: Simplifies making HTTP requests.
- prompt_toolkit: Provides utilities for building interactive command line applications.

Workflow:
1. Initialize the 'Rogue' class with necessary parameters to interact with the PokeRogue API.
2. Use methods to fetch and update trainer data and gamesave slots.
3. Handle exceptions and errors during API interactions and local data operations.

Usage Example:
    # Initialize Rogue instance
    session = requests.Session()
    auth_token = "your_auth_token_here"
    rogue_instance = Rogue(session=session, auth_token=auth_token, clientSessionId="your_session_id_here")

    # Fetch trainer data
    trainer_data = rogue_instance.get_trainer_data()

    # Update gamesave slot
    rogue_instance.update_gamesave_slot(slot=1, data={"key": "value"})

Output Example:
    - Successful fetching of trainer data.
    - Error handling messages for failed API requests.

Modules/Librarys used and for what purpose exactly in each function:
- json: Parsing and serializing JSON data for API responses.
- random: Generating random numbers for various utilities.
- os: Interfacing with the operating system for file and directory operations.
- shutil: Managing file operations such as copying and deleting files.
- time: Handling timing operations and delays in script execution.
- logging: Logging events and errors during script execution.
- colorama.Style: Styling terminal output for improved readability.
- re: Utilizing regular expressions for text processing and matching.
- datetime: Manipulating dates and times for timestamping and scheduling operations.
- requests: Making HTTP requests to interact with the PokeRogue API.
- prompt_toolkit: Building interactive command-line interfaces for user interactions.
"""
# Import custom Exceptions
from modules.handler import handle_operation_exceptions, OperationError, OperationSuccessful, OperationCancel, PropagateResponse, OperationSoftCancel  # noqa: F401
from modules.handler import handle_http_exceptions, HTTPEmptyResponse  # noqa: F401

from modules import handle_error_response, HeaderGenerator, config
from utilities import Generator, EnumLoader, cFormatter, Color, Limiter, eggLogic

from enum import Enum
import json
import random
import os
import shutil
import time
from typing import Dict, Any, Optional, List
from time import sleep
import logging
from datetime import datetime
from requests.exceptions import SSLError, ConnectionError, Timeout
import requests
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from sys import exit
import re
#import zstandard as zstd
from colorama import Style
limiter = Limiter(lockout_period=40, timestamp_file='./data/extra.json')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
#global_compressor = zstd.ZstdCompressor()
#global_decompressor = zstd.ZstdDecompressor()

class Rogue:
    """
    A class to interact with the PokeRogue API for managing trainer and gamesave data.

    Attributes:
        TRAINER_DATA_URL (str): The URL to fetch trainer data from the API.
        GAMESAVE_SLOT_URL (str): The base URL to fetch gamesave data from a specific slot from the API.
        UPDATE_TRAINER_DATA_URL (str): The URL to update trainer data on the API.
        UPDATE_GAMESAVE_SLOT_URL (str): The base URL to update gamesave data for a specific slot on the API.
    """

    TRAINER_DATA_URL = 'https://api.pokerogue.net/savedata/system/get?clientSessionId='
    GAMESAVE_SLOT_URL = 'https://api.pokerogue.net/savedata/session/get?slot='
    UPDATE_TRAINER_DATA_URL = 'https://api.pokerogue.net/savedata/update?datatype=0'
    UPDATE_GAMESAVE_SLOT_URL = 'https://api.pokerogue.net/savedata/update?datatype=1&slot='
    UPDATE_ALL_URL = 'https://api.pokerogue.net/savedata/updateall'
    LOGOUT_URL = 'https://api.pokerogue.net/account/logout'

    def __init__(self, session: requests.Session, auth_token: str, clientSessionId: str = None, driver: dict = None, useScripts: Optional[bool] = None, editOffline: bool=False) -> None:
        """
        Initializes the Rogue class instance.

        :args:
            session (requests.Session): The requests session object for making HTTP requests.
            auth_token (str): Authentication token for accessing the PokeRogue API.
            clientSessionId (str, optional): Client session ID for API authentication.
            driver (dict, optional): Selenium WebDriver dictionary object (default: None).
            useScripts (bool, optional): Flag indicating whether to use custom scripts (default: None).

        :params:
            None

        Usage Example:
            session = requests.Session()
            auth_token = "your_auth_token_here"
            rogue_instance = Rogue(session=session, auth_token=auth_token, clientSessionId="your_session_id_here")

        Output Example:
            None

        Modules/Librarys used and for what purpose exactly in each function:
        - requests: Making HTTP requests to interact with the PokeRogue API.
        """
        self.slot = None
        self.session = session
        self.auth_token = auth_token
        self.clientSessionId = clientSessionId
        self.headers = self._setup_headers()
        self.__MAX_BIG_INT = (2 ** 53) - 1
        self.driver = driver
        self.useScripts = useScripts

        self.secretId = None
        self.trainerId = None

        self.generator = Generator()
        self.generator.generate()
        self.appData = EnumLoader()

        self.backup_dir = config.backupDirectory
        self.data_dir = config.dataDirectory

        self.pokemon_id_by_name, self.biomesByID, self.moves_by_id, self.natureData, self.vouchers_data, self.natureSlot_data = self.appData.f_convertToEnums()
        self.editOffline = editOffline
        try:
            with open(f'{self.data_dir}/extra.json') as f:
                self.extra_data = json.load(f)
            
            with open(f'{self.data_dir}/passive.json') as f:
                self.passive_data = json.load(f)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Something on inital data generation failed. {e}', isLogging=True)
        
        self.__dump_data()

    
    """    
    def __compress_zstd(data, encoding='utf-8'):
            compressor = zstd.ZstdCompressor()
            compressed_data = compressor.compress(data.encode(encoding))
            return compressed_data

    def __decompress_zstd(compressed_data, encoding='utf-8'):
        decompressor = zstd.ZstdDecompressor()
        decompressed_data = decompressor.decompress(compressed_data)
        return decompressed_data.decode(encoding)"""

    def _make_request(self, url: str, method: str = 'GET', data: Optional[Dict[str, Any]] = None) -> str:
        """
        Makes an HTTP request using the Selenium WebDriver.

        :args:
            url (str): The URL to make the request to.
            method (str, optional): The HTTP method (default is 'GET').
            data (dict, optional): The payload for POST requests.

        :params:
            None

        Usage Example:
            response = self._make_request('https://api.pokerogue.net/savedata/system/get?clientSessionId=1234', method='GET')

        Output Example:
            'Successfully fetched data.'

        Modules/Librarys used and for what purpose exactly in each function:
        - requests: Making HTTP requests to interact with the PokeRogue API.
        """
        method = json.dumps(method)
        url = json.dumps(url)

        script = f"""
            var callback = arguments[0];
            var xhr = new XMLHttpRequest();
            xhr.open({method}, {url}, true);
        """

        if self.headers:
            for key, value in self.headers.items():
                key = json.dumps(key)
                value = json.dumps(value)
                script += f'xhr.setRequestHeader({key}, {value});'
        
        if data:
            data = json.dumps(data)
            script += f'xhr.send({data});'
        else:
            script += 'xhr.send();'

        script += """
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    callback(xhr.responseText);
                }
            };
        """

        return self.driver.execute_async_script(script)

    def _setup_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Generates random headers for the session.

        :args:
            None

        :params:
            headers (Dict[str, str], optional): Custom headers to include (default: None).

        Usage Example:
            headers = self._setup_headers()
            print(headers)

        Output Example:
            {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'your_auth_token_here'}

        Modules/Librarys used and for what purpose exactly in each function:
        - HeaderGenerator: Generates headers for HTTP requests.
        """
        if not headers:
            headers = HeaderGenerator.generate_headers()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = self.auth_token

        return headers
    
    def __dump_data(self, slot: int = 1) -> None:
        """
        Dump data from the API to local files.

        :args:
            slot (int, optional): The slot number (1-5). Defaults to 1.

        :params:
            None

        Usage Example:
            self.__dump_data(slot=3)
        Usage Example (continued):
            self.__dump_data(slot=3)

        Output Example:
            Successful backup creation and local data dump.

        Modules/Librarys used and for what purpose exactly in each function:
        - EnumLoader: Loads and converts data into enums for structured storage and retrieval.
        - config: Provides configuration settings, such as directories for backups and data storage.
        - json: Handles JSON data operations for reading and writing local data files.
        - cFormatter: Formats console output with colors and styles for better readability.
        - Color: Defines color constants for styling console messages.

        Exceptions:
        - If the specified slot is out of range (1-5), an "Invalid input" message is printed.

        """
        try:
            while not self.slot or self.slot > 5 or self.slot < 1:
                slot = int(input('Enter slot (1-5): '))
                self.slot = slot
                if self.slot > 5 or self.slot < 1:
                    cFormatter.print(Color.INFO, 'Invalid input. Slot number must be between 1 and 5.')
            if self.editOffline:
                gameData = self.__loadDataFromJSON('trainer.json')
                slotData = self.__loadDataFromJSON(f'slot_{slot}.json')
                self.trainerId = gameData.get('trainerId')
                self.secretId = gameData.get('secretId')
            else:
                gameData = self.get_trainer_data()
                slotData = self.getSlotData(slot)
                self.trainerId = gameData.get('trainerId')
                self.secretId = gameData.get('secretId')

            if slotData and gameData:
                self.f_createBackup()

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function __dump_data(): {e}', isLogging=True)

    # TODO IMPORTANT: Simplify
    @limiter.lockout
    def get_trainer_data(self) -> dict:
        """
        Fetch trainer data from the API.

        Returns:
            dict: Trainer data from the API.

        :args:
            None

        :params:
            None

        Usage Example:
            trainer_data = self.get_trainer_data()
            print(trainer_data)

        Output Example:
            {'trainerId': '1234', 'name': 'Ash Ketchum', ...}

        Modules/Librarys used and for what purpose exactly in each function:
        - requests: Makes HTTP requests to retrieve trainer data from the PokeRogue API.
        - cFormatter: Formats console output with colors and styles for better readability.
        - Color: Defines color constants for styling console messages.

        Exceptions:
        - Handles various errors, such as network issues or invalid responses, by printing debug information.
        """
        cFormatter.print(Color.INFO, 'Fetching trainer data...')
        if self.useScripts:
            try:
                response = self._make_request(f'{self.TRAINER_DATA_URL}{self.clientSessionId}')
                if response:
                    try:
                        # TODO MAYBE: zstandart compression, was in a migration on the server at some point
                        # but they reverted it, lets keep it so we know already
                        # decompressed_data = self.__decompress_zstd(response)
                        # data = json.loads(decompressed_data)
                        data = json.loads(response)
                        self.__writeJSONData(data, 'trainer.json', False)
                        cFormatter.print(Color.GREEN, 'Successfully fetched trainer data.')
                        return data
                    except json.JSONDecodeError as e:
                        cFormatter.print(Color.WARNING, f"Error decoding JSON: {e}", isLogging=True)
                        cFormatter.print(Color.WARNING, f"Unexpected response format: {response}", isLogging=True)
                else:
                    cFormatter.print(Color.WARNING, "The request appeared to be empty.")
            except Exception as e:
                cFormatter.print(Color.CRITICAL, f"Error in function get_trainer_data(): {e}", isLogging=True)
        else:
            try:
                response = self.session.get(f'{self.TRAINER_DATA_URL}{self.clientSessionId}', headers=self.headers)
                response.raise_for_status()
                if response.content:  # Check if the response content is not empty
                    cFormatter.print(Color.GREEN, 'Successfully fetched trainer data.')
                    data = response.json()
                    self.trainerId = data.get('trainerId')
                    self.secretId = data.get('secretId')
                    self.__writeJSONData(data, 'trainer.json', False)
                    return data
                else:
                    return handle_error_response(response)
            except requests.RequestException as e:
                cFormatter.print(Color.DEBUG, f'Error fetching trainer data. Please restart the tool. \n {e}', isLogging=True)

    # TODO IMPORTNAT: Simplify
    def getSlotData(self, slot: int = 1) -> Optional[Dict[str, Any]]:
        """
        Fetch gamesave data from the API for a specified slot.

        Args:
            slot (int, optional): The slot number (1-5). Defaults to 1.

        Returns:
            dict or None: Gamesave data retrieved from the API, or None if unsuccessful.

        Example:
            >>> rogue_instance.get_gamesave_data(2)
            # Output:
            # {
            #   "slotId": 2,
            #   "pokemonData": [...],
            #   "itemData": [...],
            #   ...
            # }

        Modules/Librarys used and for what purpose exactly in each function:
            - requests: Used for making HTTP requests to the API to fetch gamesave data.
            - cFormatter, Color: Used for formatting and printing colored output messages.
            - handle_error_response: Used to handle and process error responses from API requests.
        """
        cFormatter.print(Color.INFO, f'Fetching data for Slot {slot}...')
        
        if self.useScripts:
            try:
                response = self._make_request(f'{self.GAMESAVE_SLOT_URL}{slot-1}&clientSessionId={self.clientSessionId}')
                if response:
                    try:
                        # TODO MAYBE: zstandart compression, was in a migration on the server at some point
                        # but they reverted it, lets keep it so we know already
                        #decompressed_data = self.__decompress_zstd(response)
                        #data = json.loads(decompressed_data)
                        data = json.loads(response)
                        self.__writeJSONData(data, f'slot_{slot}.json', False)
                        self.slot = slot
                        return data
                    except json.JSONDecodeError as e:
                        cFormatter.print(Color.WARNING, f'Error decoding JSON: {e}', isLogging=True)
                        cFormatter.print(Color.WARNING, f'Unexpected response format: {response}', isLogging=True)
            except Exception as e:
                cFormatter.print(Color.CRITICAL, f'Error in function get_gamesave_data(): {e}', isLogging=True)
        else:
            try:
                response = self.session.get(f'{self.GAMESAVE_SLOT_URL}{slot-1}&clientSessionId={self.clientSessionId}', headers=self.headers)
                response.raise_for_status()
                if response.content:  # Check if the response content is not empty
                    cFormatter.print(Color.GREEN, f'Successfully fetched data for slot {self.slot}.')
                    data = response.json()
                    self.__writeJSONData(data, f'slot_{slot}.json', False)
                    self.slot = slot
                    return data
                else:
                    return handle_error_response(response)
            except requests.RequestException as e:
                cFormatter.print(Color.CRITICAL, f'Error fetching save-slot data. Please restart the tool. \n {e}', isLogging=True)

    def logout(self) -> None:
        """
        Logout from the PokeRogue API session.

        Logs out the current session and optionally closes resources like WebDriver.

        Args:
            None

        Returns:
            None

        Example:
            >>> rogue_instance.logout()
            # Output:
            # Terminating session, logging out.
            # Session terminated successfully.

        Modules/Librarys used and for what purpose exactly in each function:
            - requests: Used for making HTTP requests to logout from the API.
            - cFormatter, Color: Used for formatting and printing colored output messages.
        """
        cFormatter.print(Color.INFO, 'Terminating session, logging out.')
        
        try:
            self.session.get(f'{self.LOGOUT_URL}', headers=self.headers)
            if not self.driver and not self.useScripts:
                self.session.close()
            if self.useScripts:
                self.driver.quit()
            cFormatter.print(Color.BRIGHT_GREEN, 'Session terminated successfully.')
            sleep(5)
            exit(0)
        except Exception as e:
            cFormatter.print(Color.WARNING, f'Error logging out. {e}')

    def __writeJSONData(self, data: Dict[str, Any], filename: str, showSuccess: bool = True) -> None:
        """
        Write data to a JSON file.

        Args:
            data (Dict[str, Any]): The data to write.
            filename (str): The name of the file.
            showSuccess (bool, optional): Flag to print success message. Defaults to True.

        Returns:
            None

        Example:
            >>> rogue_instance.__write_data(data, 'trainer.json')
            # Output:
            # Written to local data. Do not forget to apply to server when done!

        Modules/Librarys used and for what purpose exactly in each function:
            - json: Used for serializing data into JSON format and writing to a file.
            - cFormatter, Color: Used for formatting and printing colored output messages.
        """
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
                if showSuccess:
                    cFormatter.print(Color.BRIGHT_GREEN, 'Written to local data. Do not forget to apply to server when done!')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function __write_data(): {e}', isLogging=True)

    def __loadDataFromJSON(self, file_path: str) -> Dict[str, Any]:
        """
        Load data from a specified file path.

        Args:
            file_path (str): Path to the file to be loaded.

        Returns:
            dict: Loaded data from the specified file.

        Example:
            >>> rogue_instance.__load_data('trainer.json')
            # Output:
            # Loaded data as a dictionary.

        Raises:
            Exception: If any error occurs during the process.

        Modules/Librarys used and for what purpose exactly in each function:
            - json: Used for deserializing data from JSON format.
            - cFormatter, Color: Used for formatting and printing colored output messages.
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function __load_data(): {e}', isLogging=True)

    def f_createBackup(self, offline: bool = False) -> None:
        """
        Create a backup of JSON files.

        What it does:
        - Creates a backup of all JSON files in the current directory to `config.backupsDirectory`.
        - Uses a timestamped naming convention for backup files (`backup_{trainerid}_{timestamp}.json`).
        - Prints 'Backup created.' upon successful backup completion.

        :args: None
        :params: None

        Usage Example:
            instance.f_createBackup()

        Output Example:
            # Output: backup/backup_{trainerid}_{timestamp}.json
            # Backup created.

        Modules/Librarys used and for what purpose exactly in each function:
        - os: For directory creation and file handling operations.
        - json: For loading JSON data from files.
        - shutil: For copying files from the current directory to the backup directory.
        - datetime: For generating timestamps for backup file names.
        """
        if config.debugDeactivateBackup:
            return

        backupDirectory =  config.backupDirectory
        if not os.path.exists(backupDirectory):
            os.makedirs(backupDirectory)

        for file in os.listdir('.'):
            if file.endswith('.json'):
                with open(file, 'r') as f:
                    data = json.load(f)
                trainerId = data.get('trainerId')
                if trainerId is not None:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    baseFilename = f'base_{trainerId}.json'
                    baseFilepath = os.path.join(backupDirectory, baseFilename)

                    if os.path.exists(baseFilepath):
                        backupFilename = f'backup_{trainerId}_{timestamp}.json'
                        backupFilepath = os.path.join(backupDirectory, backupFilename)
                        shutil.copy(file, backupFilepath)
                    else:
                        shutil.copy(file, baseFilepath)
                    cFormatter.print(Color.GREEN, 'Backup created.')

    @handle_operation_exceptions
    def f_restoreBackup(self) -> None:
        """
        Restore a backup of JSON files and update the timestamp in trainer.json.

        What it does:
        - Restores a selected backup file (`backup_{trainerid}_{timestamp}.json` or `backup_{trainerid}_slot_{slotnumber}_{timestamp}.json`) to the appropriate target file.
        - Updates the timestamp in the target file with the current timestamp upon restoration.
        - Displays a numbered list of available backup files matching the current trainer ID for selection.
        - Prompts the user to choose a backup file to restore and handles user input validation.
        - Prints 'Data restored.' upon successful restoration.

        :args: None
        :params: None

        Usage Example:
            instance.restore_backup()

        Output Example:
            # Output:
            # 1: base_123.json         <- Created on first edit
            # 2: backup_123_20230101_121212.json
            # 3: backup_123_slot_1_090413.json
            # Enter the number of the file you want to restore: 2
            # Data restored.

        Modules/Librarys used and for what purpose exactly in each function:
        - os: For directory listing and file handling operations.
        - re: For filtering and sorting backup files based on trainer ID patterns.
        - shutil: For copying files from the backup directory to the target file.
        - datetime: For generating timestamps and updating timestamps in the target file.
        """
        backupDirectory = config.backupDirectory
        files = os.listdir(backupDirectory)

        # Filter and sort files that match trainerId
        regexPattern = f'_{self.trainerId}'
        baseFile = f'base{regexPattern}.json'
        backupFilesPattern = sorted(
            (f for f in files if re.match(rf'backup{regexPattern}(_slot_\d+)?_\d{{6,8}}(_\d{{6}})?\.json', f)),
            key=lambda x: (re.findall(r'\d+', x)[0], re.findall(r'\d{6,8}(_\d{6})?', x)[0])
        )

        # Include the base file at the top of the list if it exists
        existingFiles = [baseFile] if baseFile in files else []
        existingFiles += backupFilesPattern

        if not existingFiles:
            cFormatter.print(Color.WARNING, 'No backup files found for your trainer ID.')
            return

        # Displaying sorted list with numbers
        for idx, file in enumerate(existingFiles, 1):
            sidenote = '        <- Created on first edit' if file.startswith('base_') else ''
            print(f'{idx}: {file} {sidenote}')

        # Getting user's choice
        while True:
            choice = int(self.fh_getIntegerInput(
                promptMessage='Enter the number of the file you want to restore', 
                minBound=1, maxBound=len(existingFiles),
                zeroCancel=True
            ))
            if choice == 0:
                raise OperationCancel()
            if 1 <= choice <= len(existingFiles):
                chosenFile = existingFiles[choice - 1]
                chosenFilepath = os.path.join(backupDirectory, chosenFile)

                # Determine the output filepath
                parentDirectory = os.path.abspath(os.path.join(backupDirectory, os.pardir))

                # If the chosen file has "slot_x" in its name, determine the slot number and the corresponding target file
                matchSlot = re.search(r'_slot_(\d+)', chosenFile)
                if matchSlot:
                    dynSlot = matchSlot.group(1)
                    outputFilename = f'slot_{dynSlot}.json'
                else:
                    outputFilename = 'trainer.json'

                outputFilepath = os.path.join(parentDirectory, outputFilename)

                # Copy the chosen file to the output filepath
                shutil.copyfile(chosenFilepath, outputFilepath)

                # Read the restored file
                with open(outputFilepath, 'r') as file:
                    data = json.load(file)

                # Update the timestamp
                curTimestamp = int(datetime.now().timestamp() * 1000)
                data['timestamp'] = curTimestamp

                # Write the updated data back to the file
                with open(outputFilepath, 'w') as file:
                    json.dump(data, file, indent=4)

                cFormatter.print(Color.GREEN, 'Data restored and timestamp updated.')
                break


    # TODO IMPORTANT: Simplify
    @limiter.lockout
    def update_all(self) -> None:
        """
        Update all data using the provided URL.

        What it does:
        - Uses `self.UPDATE_ALL_URL` to update data based on `trainer.json` and `slot_{slot}.json`.
        - Checks for the existence of `trainer.json` and `slot_{slot}.json` files.
        - Constructs a payload for the API request.
        - Performs an HTTP request and handles responses based on `self.useScripts`.
        - Prints specific success or error messages based on the response status.

        :args: None
        :params: None

        Usage Example:
            instance.update_all()

        Modules/Librarys used and for what purpose exactly in each function:
        - os: For checking file existence and handling file operations.
        - json: For loading JSON data from `trainer.json` and `slot_{slot}.json`.
        - random: For generating random sleep intervals.
        - requests: For making HTTP requests to the provided URL.
        """

        url = self.UPDATE_ALL_URL

        if "trainer.json" not in os.listdir():
            cFormatter.print(Color.INFO, 'trainer.json file not found!')
            return
        with open('trainer.json', 'r') as f:
            trainer_data = json.load(f)

        slot = self.slot
        if slot > 5 or slot < 1:
            cFormatter.print(Color.INFO, 'Invalid slot number')
            return
        filename = f'slot_{slot}.json'
        if filename not in os.listdir():
            cFormatter.print(Color.INFO, f'{filename} not found')
            return

        with open(filename, 'r') as f:
            game_data = json.load(f)
        try:
            sleep(random.randint(3, 5))
            payload = {'clientSessionId': self.clientSessionId, 'session': game_data, "sessionSlotId": slot - 1,
                       'system': trainer_data}
            
            # TODO MAYBE: zstandart compression, was in a migration on the server at some point
            # but they reverted it, lets keep it so we know already
            #raw_payload = {'clientSessionId': self.clientSessionId, 'session': game_data, "sessionSlotId": slot - 1, 'system': trainer_data}
            #payload = self.__compress_zstd(payload)
            if self.useScripts:
                response = self._make_request(url, method='POST', data=json.dumps(payload))
                cFormatter.print(Color.GREEN, "That seemed to work! Refresh without cache (STRG+F5)")
                self.logout()
            else:
                response = self.session.post(url=url, headers=self.headers, json=payload)
                if response.status_code == 400:
                    cFormatter.print(Color.WARNING, 'Bad Request!')
                    return
                response.raise_for_status()
                cFormatter.print(Color.GREEN, 'Updated data Successfully!')
                self.logout()
        except SSLError as ssl_err:
            cFormatter.print(Color.WARNING, f'SSL error occurred: {ssl_err}', isLogging=True)
            cFormatter.print(Color.WARNING, 'Took too long to edit, you need to be faster. Session expired.')
            sleep(5)
            self.logout()
        except ConnectionError as conn_err:
            cFormatter.print(Color.WARNING, f'Connection error occurred: {conn_err}', isLogging=True)
        except Timeout as timeout_err:
            cFormatter.print(Color.WARNING, f'Timeout error occurred: {timeout_err}', isLogging=True)
        except requests.exceptions.RequestException as e:
           cFormatter.print(Color.WARNING, f'Error occurred during request: {e}', isLogging=True)

    def f_unlockStarters(self) -> None:
        """
        Allows to unlock various options for starters and updates the local .json file.

        Args:
            None

        Raises:
            Exception: If any error occurs during the process.

        Modules Used:
        - random: For generating random values for attributes like caught and seen counts, hatched counts, and IVs.
        - json: For parsing and manipulating JSON data, specifically 'trainer.json'.
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads existing data from 'trainer.json'.
        2. Prompts the user to specify various options for starters, including forms, shininess, IVs, passive attributes,
           win ribbons, natures, cost reduction, and abilities.
        3. Uses random values for 'seenCount', 'caughtCount', 'hatchedCount', and IVs if not specified by the user.
        4. Updates 'trainer.json' with the modified starter data.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.unlock_all_starters()

        Output Example:
            - Updates 'trainer.json' with new starter data based on user inputs.
            - Prints status messages and errors using cFormatter.

        """
        try:
            trainer_data: dict = self.__loadDataFromJSON('trainer.json')

            choice: int = int(input('Do you want to unlock all forms of the pokemon? (All forms are Tier 3 shinies. 1: Yes | 2: No): '))
            if not 1 <= choice <= 2:
                cFormatter.print(Color.INFO, 'Incorrect command. Setting to NO')
                choice = 2
            caught_attr: int = self.__MAX_BIG_INT if choice == 1 else 253 if choice == 2 else \
                               int(input('Make the Pokemon shiny? (1: Yes, 2: No): '))

            if not 1 <= choice <= 2:
                cFormatter.print(Color.INFO, 'Invalid choice. Setting to NO')
                choice = 2
            elif choice == 2:
                caught_attr = 253
            else:
                choice: int = int(input('What tier shiny do you want? (1: Tier 1, 2: Tier 2, 3: Tier 3, 4: All shinies): '))
                if not 1 <= choice <= 4:
                    cFormatter.print(Color.INFO, 'Invalid choice.')
                    return
                elif choice == 1:
                    caught_attr = 159
                elif choice == 2:
                    caught_attr = 191
                elif choice == 3:
                    caught_attr = 223
                else:
                    caught_attr = 255
            
            iv: int = int(input('Do you want the starters to have perfect IVs? (1: Yes | 2: No): '))
            if not 1 <= iv <= 2:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                iv = 2
            
            passive: int = int(input('Do you want the starters to have the passive unlocked? (1: Yes | 2: No): '))
            if not 1 <= passive <= 2:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                passive = 2
            
            ribbon: int = int(input('Do you want to unlock win-ribbons?: (1: Yes | 2: No): '))
            if not 1 <= ribbon <= 2:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                ribbon = 2

            nature: int = int(input('Do you want to unlock all natures?: (1: Yes | 2: No): '))
            if not 1 <= nature <= 2:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                nature = 2

            costReduce: int = int(input('How much do you want to reduce the cost? Yes lugia can cost nearly 0! (Number between 1 and 20): '))
            if not 0 <= costReduce <= 20:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to 0.')
                costReduce = 0

            abilityAttr: int = int(input('Do you want to unlock all abilities? (1: Yes | 2: No): '))
            if not 1 <= abilityAttr <= 2:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to none.')
                abilityAttr = 0
            elif abilityAttr == 1:
                abilityAttr = 7
            else:
                abilityAttr = 0

            total_caught: int = 0
            total_seen: int = 0
            for entry in trainer_data['dexData'].keys():
                caught: int = random.randint(100, 200)
                seen: int = random.randint(300, 400)
                hatched: int = random.randint(30, 50)
                total_caught += caught
                total_seen += seen
                randIv: List[int] = random.sample(range(20, 30), 6)

                trainer_data['dexData'][entry] = {
                    'seenAttr': 479,
                    'caughtAttr': self.__MAX_BIG_INT if choice == 1 else caught_attr,
                    'natureAttr': self.natureData.UNLOCK_ALL.value if nature == 1 else None,
                    'seenCount': seen,
                    'caughtCount': caught,
                    'hatchedCount': hatched,
                    'ivs': randIv if iv == 2 else [31, 31, 31, 31, 31, 31]
                }
                trainer_data['starterData'][entry] = {
                    'moveset': None,
                    'eggMoves': 15,
                    'candyCount': caught + 20,
                    'friendship': random.randint(1, 300),
                    'abilityAttr': abilityAttr,
                    'passiveAttr': 0 if (entry in self.passive_data['noPassive']) or (passive == 2) else 3,
                    'valueReduction': costReduce,
                    'classicWinCount': None if ribbon == 2 else 1,
                }

            self.__writeJSONData(trainer_data, 'trainer.json')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function unlock_all_starter(): {e}', isLogging=True)

    def edit_starter_separate(self, dexId: Optional[str] = None) -> None:
        """
        Allows the user to edit starter Pokemon data for a trainer.

        Args:
        - dexId (Optional[str]): The ID or name of the Pokemon. If None, the user will be prompted to enter it.

        Raises:
        - None

        Modules Used:
        - random: For generating random values for attributes like caught and seen counts, hatched counts, and IVs.
        - prompt_toolkit: For interactive command-line input and auto-completion.
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads existing data from 'trainer.json'.
        2. Allows user to input or select a Pokemon name or ID with auto-completion.
        3. Prompts user to specify various options for the selected Pokemon (forms, shininess, IVs, etc.).
        4. Updates 'trainer.json' with the modified starter data.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_starter_separate()

        """
        try:
            trainer_data: dict = self.__loadDataFromJSON('trainer.json')
            
            if not dexId:
                pokemon_completer: WordCompleter = WordCompleter(self.pokemon_id_by_name.__members__.keys(), ignore_case=True)

                cFormatter.print(Color.INFO, 'Write the name of the pokemon, it will recommend for auto-completion.')
                dexId: str = prompt('Enter Pokemon (Name / ID): ', completer=pokemon_completer)
                
                if dexId.isnumeric():
                    if dexId not in trainer_data['starterData']:
                        cFormatter.print(Color.INFO, f'No pokemon with ID: {dexId}')
                        return
                else:
                    try:
                        dexId: str = self.pokemon_id_by_name[dexId.lower()].value
                    except KeyError:
                        cFormatter.print(Color.INFO, f'No pokemon with ID: {dexId}')
                        return

            choice: int = int(input('Do you want to unlock all forms of the pokemon? (All forms are Tier 3 shinies. 1: Yes, 2: No): '))
            if not 1 <= choice <= 2:
                cFormatter.print(Color.INFO, f'No pokemon with ID: {dexId}')
                return
            elif choice == 1:
                caught_attr: int = self.__MAX_BIG_INT
            else:
                choice: int = int(input('Make the Pokemon shiny? (1: Yes, 2: No): '))

                if not 1 <= choice <= 2:
                    cFormatter.print(Color.INFO, 'Invalid choice. Setting to NO')
                    choice
                elif choice == 2:
                    caught_attr = 253
                else:
                    choice: int = int(input('What tier shiny do you want? (1: Tier 1, 2: Tier 2, 3: Tier 3, 4: All shinies): '))
                    if not 1 <= choice <= 4:
                        cFormatter.print(Color.INFO, 'Invalid choice.')
                        return
                    elif choice == 1:
                        caught_attr = 159
                    elif choice == 2:
                        caught_attr = 191
                    elif choice == 3:
                        caught_attr = 223
                    else:
                        caught_attr = 255
                
            caught: int = int(input('How many of this Pokemon have you caught?: '))
            hatched: int = int(input('How many of this Pokemon have hatched from eggs?: '))
            seen_count: int = int(input('How many of this Pokemon have you seen?: '))
            candies: int = int(input('How many candies do you want?: '))
            cFormatter.print(Color.INFO, 'Choose a value between 1 and 31 for your IVs (Pokemon Stats).')
            ivs: list[int] = [int(input('SpA IVs: ')), int(input('DEF IVs: ')), int(input('Attack IVs: ')),
                int(input('HP IVs: ')), int(input('Spe IVs: ')), int(input('Def IVs: '))]

            passive: int = int(input('Do you want the starters to have the passive unlocked? (1: Yes | 2: No): '))
            if not 1 <= passive <= 2:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                passive = 2
            elif passive == 1:
                if dexId in self.passive_data['noPassive']:
                    cFormatter.print(Color.INFO, 'This pokemon has no passive.')
                    passiveAttr: int = 0
                else:
                    passiveAttr: int = 3
            else:
                passiveAttr: int = 0
            
            costReduce: int = int(input('How much do you want to reduce the cost? Yes lugia can cost nearly 0! (Number between 1 and 20): '))
            if not 0 <= costReduce <= 20:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to 0.')
                costReduce = 0

            abilityAttr: int = int(input('Do you want to unlock all abilities? (1: Yes, with hidden | 2: No): '))
            if not 1 <= abilityAttr <= 2:
                cFormatter.print(Color.INFO, 'Invalid input. Setting to none.')
                abilityAttr = 0
            elif abilityAttr == 1:
                abilityAttr = 7
            else:
                abilityAttr = 0
            
            self.legacy_natures()

            nature_completer: WordCompleter = WordCompleter(self.natureData.__members__.keys(), ignore_case=True)
            
            cFormatter.print(Color.BRIGHT_YELLOW, 'Write the name of the nature, it will recommend for auto-completion.')
            nature: str = prompt('What nature would you like?: ', completer=nature_completer)

            nature: int = self.natureData[nature].value

            trainer_data['dexData'][str(dexId)] = {
                'seenAttr': 479,
                'caughtAttr': caught_attr,
                'natureAttr': nature,
                'seenCount': seen_count,
                'caughtCount': caught,
                'hatchedCount': hatched,
                'ivs': ivs
            }
            trainer_data['starterData'][dexId] = {
                'moveset': None,
                'eggMoves': 15,
                'candyCount': candies,
                'abilityAttr': abilityAttr,
                'passiveAttr': passiveAttr,
                'valueReduction': costReduce
            }

            self.__writeJSONData(trainer_data, 'trainer.json')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_starters(): {e}', isLogging=True)

    def add_ticket(self) -> None:
        """
        Simulates an egg gacha.

        Allows the user to input the number of common, rare, epic, and legendary vouchers they want to use.
        Updates the voucher counts in the trainer data.

        Returns:
        - None

        Raises:
        - None

        Modules Used:
        - prompt_toolkit: For interactive command-line input.
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads existing data from 'trainer.json'.
        2. Prompts user to input the number of common, rare, epic, and legendary vouchers.
        3. Updates 'trainer.json' with the new voucher counts.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.add_ticket()

        """
        try:
            trainer_data = self.__loadDataFromJSON('trainer.json')

            common: int = int(input('How many common vouchers do you want: '))

            rare: int = int(input('How many rare vouchers do you want: '))

            epic: int = int(input('How many epic vouchers do you want: '))

            legendary: int = int(input('How many legendary vouchers do you want: '))

            voucher_counts: dict[str, int] = {
                '0': common,
                '1': rare,
                '2': epic,
                '3': legendary
            }
            trainer_data['voucherCounts'] = voucher_counts

            self.__writeJSONData(trainer_data, 'trainer.json')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function add_tickets(): {e}', isLogging=True)

    def edit_pokemon_party(self) -> None:
        """
        Allows the user to edit the Pokemon party.

        Raises:
        - None

        Modules Used:
        - prompt_toolkit: For interactive command-line input and auto-completion.
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads game data based on the current slot.
        2. Allows the user to select a party slot and choose from various options to edit a Pokemon's attributes.
        3. Updates the game data with the modified Pokemon attributes.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_pokemon_party()

        """
        try:
            slot = self.slot
            filename = f'slot_{slot}.json'

            game_data = self.__loadDataFromJSON(filename)

            if game_data['gameMode'] == 3:
                cFormatter.print(Color.BRIGHT_YELLOW, 'Cannot edit this property on Daily Runs.')
                return

            options = [
                '1: Change species',
                '2: Set it shiny',
                '3: Set Level',
                '4: Set Luck',
                '5: Set IVs',
                '6: Change a move on a pokemon in your team',
                '7: Change nature of a pokemon in your team'
            ]

            party_num = int(input('Select the party slot of the Pokémon you want to edit (0-5): '))
            if party_num < 0 or party_num > 5:
                cFormatter.print(Color.BRIGHT_YELLOW, 'Invalid party slot.')
                return

            cFormatter.fh_printSeperators(65, '-', Color.WHITE)
            cFormatter.print(Color.WHITE, '\n'.join(options))
            cFormatter.fh_printSeperators(65, '-', Color.WHITE)

            command = int(input('Option: '))
            if command < 1 or command > 7:
                cFormatter.print(Color.INFO, 'Invalid input.')
                return

            if command == 1:
                pokemon_completer: WordCompleter = WordCompleter(self.pokemon_id_by_name.__members__.keys(), ignore_case=True)
                cFormatter.print(Color.INFO, 'Write the name of the pokemon, it will recommend for auto-completion.')
                dexId: str = prompt('Enter Pokemon (Name / ID): ', completer=pokemon_completer)
                
                try:
                    dexId: str = self.pokemon_id_by_name[dexId.lower()].value
                except KeyError:
                    cFormatter.print(Color.INFO, f'No Pokemon with Name: {dexId}')
                    return
                game_data['party'][party_num]['species'] = int(dexId)

            elif command == 2:
                game_data['party'][party_num]['shiny'] = True
                variant = int(input('Choose the shiny variant (from 0 to 2): '))
                if variant < 0 or variant > 2:
                    cFormatter.print(Color.INFO, 'Invalid input.')
                    return
                game_data['party'][party_num]['variant'] = variant
            elif command == 3:
                level = int(input('Choose the level: '))
                if level < 1:
                    cFormatter.print(Color.INFO, 'Invalid input.')
                    return
                game_data['party'][party_num]['level'] = level
            elif command == 4:
                luck = int(input('What luck level do you desire? (from 1 to 14): '))
                if luck < 1 or luck > 14:
                    cFormatter.print(Color.INFO, 'Invalid input.')
                    return
                game_data['party'][party_num]['luck'] = luck
            elif command == 5:
                ivs = [int(input('SpA IVs: ')), int(input('DEF IVs: ')), int(input('Attack IVs: ')),
                    int(input('HP IVs: ')), int(input('Spe IVs: ')), int(input('Def IVs: '))]
                game_data['party'][party_num]['ivs'] = ivs
            elif command == 6:
                move_slot = int(input('Select the move you want to change (from 0 to 3): '))
                if move_slot < 0 or move_slot > 3:
                    cFormatter.print(Color.INFO, 'Invalid input.')
                    return
                
                self.legacy_moves()

                move_completer: WordCompleter = WordCompleter(self.moves_by_id.__members__.keys(), ignore_case=True)
                
                cFormatter.print(Color.INFO, 'Write the name of the move, it will recommend for auto completion.')
                move: str = prompt('What move would you like?: ', completer=move_completer)

                move: int = int(self.moves_by_id[move].value)
            
                game_data['party'][party_num]['moveset'][move_slot]['moveId'] = move
            else:
                self.legacy_natureSlot()

                natureSlot_completer: WordCompleter = WordCompleter(self.natureSlot_data.__members__.keys(), ignore_case=True)
                cFormatter.print(Color.INFO, 'Write the name of the nature, it will recommend for auto-completion.')
                natureSlot: str = prompt('What nature would you like?: ', completer=natureSlot_completer)

                natureSlot: int = int(self.natureSlot_data[natureSlot].value)
            
                game_data['party'][party_num]['nature'] = natureSlot

            self.__writeJSONData(game_data, filename)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_pokemon_party(): {e}', isLogging=True)

    def f_editGamemodes(self) -> None:
        """
        Unlocks all game modes for the player.

        Raises:
        - None

        Modules Used:
        - None

        Workflow:
        1. Loads the trainer data.
        2. Unlocks all game modes for the player in the game data.
        3. Updates the game data with the unlocked game modes.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.unlock_all_gamemodes()

        """
        try:
            trainer_data = self.__loadDataFromJSON('trainer.json')

            unlocked_modes = trainer_data.get('unlocks', {})
            if not unlocked_modes:
                cFormatter.print(Color.INFO, 'Unable to find data entry: unlocks')
                return

            for mode in unlocked_modes:
                unlocked_modes[mode] = True

            self.__writeJSONData(trainer_data, 'trainer.json')
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function unlock_all_gamemodes(): {e}', isLogging=True)

    def f_editAchivements(self) -> None:
        """
        Unlocks all achievements for the player.

        Raises:
        - None

        Modules Used:
        - time: For generating current timestamp.
        - random: For generating random unlock times.
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads trainer data and retrieves achievement data.
        2. Generates random unlock times for each achievement and updates the game data accordingly.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.unlock_all_achievements()

        """
        try:
            trainer_data = self.__loadDataFromJSON('trainer.json')

            current_time_ms = int(time.time() * 1000) 
            min_time_ms = current_time_ms - 3600 * 1000  

            achievements = self.extra_data['achievements']
            trainer_data['achvUnlocks'] = {
                achievement: random.randint(min_time_ms, current_time_ms)
                for achievement in achievements
            }

            self.__writeJSONData(trainer_data, 'trainer.json')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function unlock_all_achievements(): {e}', isLogging=True)

    def f_editVouchers(self) -> None:
        """
        Unlocks all vouchers for the player or a specific voucher with random unlock times.

        Raises:
        - None

        Modules Used:
        - random: For generating random unlock times.
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads trainer data.
        2. Allows the user to choose to unlock all vouchers or a specific voucher with random unlock times.
        3. Updates the game data with the unlocked voucher information.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_vouchers()

        """
        try:
            gameData = self.__loadDataFromJSON('trainer.json')

            currentTime = int(time.time() * 1000) 
            minBoundaryTime = currentTime - 3600 * 1000  
            

            choice: int = int(input('Do you want to unlock all vouchers or unlock a specific voucher? (1: All | 2: Specific): '))

            if (choice < 1) or (choice > 2):
                cFormatter.print(Color.INFO, 'Invalid command.')
                return
            elif choice == 1:
                keysToUpdate = {}
                for voucher in self.vouchers_data.__members__:
                    randomTime = minBoundaryTime + random.randint(0, currentTime - minBoundaryTime)
                    keysToUpdate[voucher] = randomTime
                gameData['voucherUnlocks'] = keysToUpdate
            else:
                self.legacy_vouchers()
                vouchersCompleter: WordCompleter = WordCompleter(self.vouchers_data.__members__.keys(), ignore_case=True)
                cFormatter.print(Color.INFO, 'Write the name of the voucher, it will recommend for auto-completion.')
            
                vouchers: str = prompt('What voucher would you like?: ', completer=vouchersCompleter)

                if 'voucherUnlocks' in gameData and vouchers in gameData['voucherUnlocks']:
                    randomTime = minBoundaryTime + random.randint(0, currentTime - minBoundaryTime)
                    gameData['voucherUnlocks'][vouchers] = randomTime
                else:
                    randomTime = minBoundaryTime + random.randint(0, currentTime - minBoundaryTime)
                    gameData['voucherUnlocks'][vouchers] = randomTime

            self.__writeJSONData(gameData, 'trainer.json')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_vouchers(): {e}', isLogging=True)

    def legacy_pokedex(self) -> None:
        pokemons = [f'{member.value}: {member.name}' for member in self.pokemon_id_by_name]
        cFormatter.print(Color.WHITE, '\n'.join(pokemons))
        
    def legacy_printBiomes(self) -> None:
        biomes = [f'{member.value}: {member.name}' for member in self.biomesByID]
        cFormatter.print(Color.WHITE, '\n'.join(biomes))

    def legacy_moves(self) -> None:
        moves = [f'{member.value}: {member.name}' for member in self.moves_by_id]
        cFormatter.print(Color.WHITE, '\n'.join(moves))

    def legacy_natures(self) -> None:  
        natures = [f'{member.value}: {member.name}' for member in self.natureData]
        cFormatter.print(Color.WHITE, '\n'.join(natures))
        
    def legacy_vouchers(self) -> None:
        vouchers = [f'{member.value}: {member.name}' for member in self.vouchers_data]
        cFormatter.print(Color.WHITE, '\n'.join(vouchers))

    def legacy_natureSlot(self) -> None:
        natureSlot = [f'{member.value}: {member.name}' for member in self.natureSlot_data]
        cFormatter.print(Color.WHITE, '\n'.join(natureSlot))

    @handle_operation_exceptions
    def f_addCandies(self) -> None:
        """
        Args:
        - dexId (str, optional): The ID of the Pokémon. Defaults to None.

        Adds candies to a Pokémon.

        Raises:
        - Exception: If any error occurs during the process due to the decorator.
        - OperationCancel(), OperationSoftCancel(), ValueError() depending on input due to the helper.
        raise OperationSuccessful(f'Added {candies} candies to {pokeName}.')

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads trainer data.
        2. Allows the player to specify a Pokémon by name or ID (optional).
        3. Allows the player to input the number of candies to add to the Pokémon.
        4. Updates the game data with the new candy count for the Pokémon.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.f_addCandies('pikachu')
        """

        trainerData = self.__loadDataFromJSON('trainer.json')

        cFormatter.print(Color.DEBUG, 'Write the name of the Pokémon or its ID.')

        inputValue = self.fh_getCompleterInput(
            promptMessage='Choose which pokemon: ',
            choices={**{member.name.lower(): member for member in self.appData.pokemonIDByName}, 
                     **{str(member.value): member for member in self.appData.pokemonIDByName}},
            zeroCancel=False
        )
        pokeName = inputValue.name.lower()

        # Prompt for number of candies using fh_getIntegerInput method
        candies = self.fh_getIntegerInput(
            promptMessage='How many candies do you want to add (0 to cancel): ',
            minBound=0,
            maxBound=999,  # Adjust maximum candies as needed
            zeroCancel=True
        )

        # Update game data with the chosen Pokémon's candy count
        trainerData["starterData"][inputValue.value]["candyCount"] = candies

        # Write updated data to JSON
        self.__writeJSONData(trainerData, 'trainer.json')
        raise OperationSuccessful(f'Added {candies} candies to {pokeName}.')

    @handle_operation_exceptions
    def f_editBiome(self) -> None:
        """
        Edits the biome of the game using helper functions for input validation and word completion.

        Raises:
        - Exception: If any error occurs during the process due to the decorator.
        - OperationCancel(), OperationSoftCancel(), ValueError() depending on input due to the helper.
        - OperationSuccessful(f'Biome updated to {biomeEnum.name}')

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads game data for the current slot.
        2. Allows the player to choose a biome by name or ID using auto-completion.
        3. Updates the game data with the chosen biome ID.

        Usage Example:
            >>> example_instance = ExampleClass(1)  # Replace with actual slot number
            >>> example_instance.f_editBiome()

        """

        # Initialize EnumLoader and load enums
        gameData = self.__loadDataFromJSON(f'slot_{self.slot}.json')
        currentBiomeId = gameData["arena"]["biome"]
        currentBiomeName = next((member.name for member in self.appData.biomesByID if member.value == currentBiomeId), "Unknown")
        biomeData = self.appData.biomesByID

        # Prompt user for biome input
        self.fh_printEnums('biomes')
        cFormatter.print(Color.INFO, f'Current Biome {currentBiomeName}. You can type `exit`, `cancel` or press STRG+C to exit.')
        while True:
            try:
                inputValue = self.fh_getCompleterInput(
                    promptMessage='Choose which Biome you like. You can either type the ID or Name',
                    choices={**{member.name.lower(): member for member in biomeData}, 
                            **{str(member.value): member for member in biomeData}},
                    zeroCancel=False
                )
                break
            except KeyboardInterrupt:
                return


        # Update game data with the chosen biome ID
        gameData["arena"]["biome"] = inputValue.value
        self.__writeJSONData(gameData, f'slot_{self.slot}.json')
        raise OperationSuccessful(f'Biome updated from {currentBiomeName} to {inputValue.name}.')
            
    @handle_operation_exceptions
    def f_editPokeballs(self) -> None:
        """
        Edits the number of pokeballs in the game using helper functions for input validation.

        Raises:
        - Exception: If any error occurs during the process due to the decorator.
        - OperationCancel(), OperationSoftCancel(), ValueError() depending on input due to the helper.
        - OperationSuccessful('Successfully written Pokeballs.')
            - and prints changed items.

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads game data for the current slot.
        2. Allows the player to input the number of each type of pokeball using validated input or skip the entry.
        3. Updates the game data with the new counts for each type of pokeball.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.f_editPokeballs()
        """
        gameData = self.__loadDataFromJSON(f'slot_{self.slot}.json')

        if gameData.get("gameMode") == 3:
            cFormatter.print(Color.CRITICAL, 'Cannot edit this property on daily runs!')
            return

        pokeballTypes = {
            '0': 'Pokeball',
            '1': 'Great Balls',
            '2': 'Ultra Balls',
            '3': 'Rogue Balls',
            '4': 'Master Balls'
        }

        changed = False
        changedItems = []

        for key, name in pokeballTypes.items():
            formattedName = f'{Color.INFO}{name}{Style.RESET_ALL}'
            currentAmount = gameData.get('pokeballCounts', {}).get(key, '0')
            prompt = f'How many {formattedName}? (Currently have {currentAmount}): '
            maxBound = 999
            try:
                while True:
                    value = self.fh_getIntegerInput(prompt, 0, maxBound, softCancel=True, allowSkip=True)
                    if value == '0':
                        raise OperationSoftCancel()  # Raise OperationSoftCancel to continue the loop
                    elif value == 'skip':
                        cFormatter.print(Color.YELLOW, f'Skipping {name}...')
                        break  # Break out of the inner loop to proceed to the next item
                    else:
                        gameData.setdefault('pokeballCounts', {})[key] = int(value)
                        changedItems.append(f"{name}: {value}")
                        changed = True
                        cFormatter.print(Color.DEBUG, f'Queued {value} {name}.')
                        break  # Break out of the inner loop after successful input
            except OperationSoftCancel:
                break
        if changed:
            self.__writeJSONData(gameData, f'slot_{self.slot}.json')
            cFormatter.print(Color.YELLOW, 'Changes saved:')
            for item in changedItems:
                cFormatter.print(Color.INFO, item)
            raise OperationSuccessful('Successfully written Pokeballs.')
        else:
            cFormatter.print(Color.YELLOW, 'No changes made.')

    @handle_operation_exceptions
    def f_editMoney(self) -> None:
        """
        Edits the amount of Poke-Dollars in the game.

        Raises:
        - Exception: If any error occurs during the process due to the decorator.
        - OperationCancel(), OperationSoftCancel(), ValueError() depending on input due to the helper.
        - OperationSuccessful(f'Written {choice} as money value to to local .json.')

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads game data for the current slot.
        2. Allows the player to input the amount of Poke-Dollars they want.
        3. Updates the game data with the new amount of Poke-Dollars.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.f_editMoney()
        """
        print('test')
        saveData = self.__loadDataFromJSON(f'slot_{self.slot}.json')

        if saveData["gameMode"] == 3:
            cFormatter.print(Color.CRITICAL, 'Cannot edit this property on daily runs!')
            return

        prompt = 'How many Poke-Dollars do you want? '
        choice = self.fh_getIntegerInput(prompt, 0, float('inf'), zeroCancel=True)
        saveData["money"] = choice
        self.__writeJSONData(saveData, f'slot_{self.slot}.json')
        raise OperationSuccessful(f'Written {choice} as money value to to local .json.')

    @handle_operation_exceptions
    def f_addEggsGenerator(self) -> None:
        """
        Generates eggs for the player.

        Raises:
        - Exception: If any error occurs during the process due to the decorator.
        - OperationCancel(), OperationSoftCancel(), ValueError() depending on input due to the helper.
        - OperationSuccessful(f'{count} eggs successfully generated.')

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.
        - eggLogic: Module or class responsible for generating eggs, assumed to be imported or available.

        Workflow:
        1. Loads trainer data.
        2. If there are existing eggs, uses their structure as a sample.
        3. Allows the player to specify attributes for the eggs (count, tier, gacha type, hatch waves, shiny, hidden ability).
        4. Generates the specified number of eggs with the specified attributes.
        5. Adds the generated eggs to the player's inventory, either replacing or adding to the existing eggs.
        If there are no existing eggs, a sample structure is provided for the new eggs.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.f_addEggsGenerator()
        """
        trainerData = self.__loadDataFromJSON('trainer.json')
        currentEggs = trainerData.get('eggs', [])
        currentAmount = len(currentEggs)

        if currentAmount >= 99:
            userInput = self.fh_getChoiceInput(
                'You already have the total max of eggs, replace eggs?',
                {'1': 'Replace'}, zeroCancel=True
            )
        else:
            userInput = self.fh_getChoiceInput(
                f'You already have [{currentAmount}] eggs - should we add or replace?',
                {'1': 'Replace', '2': 'Add'}, zeroCancel=True
            )

        maxAmount = 99 - currentAmount if userInput == '2' else 99

        count = int(self.fh_getIntegerInput('How many eggs do you want to generate?', 0, maxAmount, zeroCancel=True))

        tier = int(self.fh_getChoiceInput(
            'What tier should the eggs have?',
            {'1': 'Common', '2': 'Rare', '3': 'Epic', '4': 'Legendary', '5': 'Manaphy'},
            zeroCancel=True
        )) - 1

        gachaType = int(self.fh_getChoiceInput(
            'What gacha type do you want to have?',
            {'1': 'MoveGacha', '2': 'LegendaryGacha', '3': 'ShinyGacha'}, zeroCancel=True
        )) - 1  # Adjusting for 0-based index

        hatchWaves = self.fh_getIntegerInput('After how many waves should they hatch?', 0, 100, zeroCancel=True)
        
        # Get hidden ability preference as boolean
        isShiny: bool = self.fh_getChoiceInput('Do you want it to be shiny?', {'1': 'Yes', '2': 'No'}, zeroCancel=True) == '1'

        # Get hidden ability preference as boolean
        variantTier: bool = self.fh_getChoiceInput('Do you want the hidden ability to be unlocked?', {'1': 'Yes', '2': 'No'}, zeroCancel=True) == '1'

        eggDictionary = eggLogic.constructEggs(tier, gachaType, hatchWaves, count, isShiny, variantTier)

        if userInput == '1':
            trainerData['eggs'] = eggDictionary
        elif userInput == '2':
            trainerData['eggs'].extend(eggDictionary)

        self.__writeJSONData(trainerData, 'trainer.json')
        raise OperationSuccessful(f'{count} eggs successfully generated.')

    @handle_operation_exceptions
    def f_unlockAllCombined(self) -> None:
        """
        Combines multiple functions.
        - self.f_editGamemodes()
        - self.f_editAchivements()
        - self.f_editVouchers()
        - self.f_unlockStarters()
        - self.f_editAccountStats()
        """
        self.f_editGamemodes()
        self.f_editAchivements()
        self.f_editVouchers()
        self.f_unlockStarters()
        self.f_editAccountStats()

    @handle_operation_exceptions
    def f_editAccountStats(self) -> None:
        """
        Modifies the statistics and attributes of the player's account.

        Raises:
        - Exception: If any error occurs during the process due to the decorator.
        - OperationCancel(), OperationSoftCancel(), ValueError() depending on input due to the helper.
        - OperationSuccessful('Successfully written Account Stats.')
            - and prints changed items.

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.
        - random: Standard library for generating random numbers.

        Workflow:
        1. Loads trainer data from 'trainer.json'.
        2. Generates random statistics for various gameplay attributes and updates the trainer data accordingly.
        3. Prompts the user to choose whether to randomize all values, manually enter values for each attribute, or manually enter values in a loop.
        4. Updates the gameStats based on user input.
        5. Writes the updated trainer data back to 'trainer.json'.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.f_editAccountStats()
        """
        gameData = self.__loadDataFromJSON('trainer.json')

        encounters = random.randint(100000, 200000)
        caught = round(encounters / 25)

        keysToUpdate = {
            'battles': encounters,
            'classicSessionsPlayed': random.randint(2500, 10000),
            'dailyRunSessionsPlayed': random.randint(250, 1000),
            'dailyRunSessionsWon': random.randint(50, 150),
            'eggsPulled': round(encounters / 50),
            'endlessSessionsPlayed': random.randint(100, 300),
            'epicEggsPulled': random.randint(50, 100),
            'highestDamage': random.randint(10000, 12000),
            'highestEndlessWave': random.randint(300, 1000),
            'highestHeal': random.randint(10000, 12000),
            'highestLevel': random.randint(3000, 8000),
            'highestMoney': random.randint(1000000, 10000000),
            'legendaryEggsPulled': random.randint(10, 50),
            'legendaryPokemonCaught': random.randint(25, 100),
            'legendaryPokemonHatched': random.randint(25, 100),
            'legendaryPokemonSeen': random.randint(2500, 10000),
            'manaphyEggsPulled': random.randint(5, 10),
            'mythicalPokemonCaught': random.randint(20, 70),
            'mythicalPokemonHatched': random.randint(20, 70),
            'mythicalPokemonSeen': random.randint(20, 70),
            'pokemonCaught': caught,
            'pokemonDefeated': random.randint(2500, 10000),
            'pokemonFused': random.randint(50, 150),
            'pokemonHatched': random.randint(2500, 10000),
            'pokemonSeen': random.randint((encounters-1500), (encounters-500)),
            'rareEggsPulled': random.randint(150, 250),
            'ribbonsOwned': random.randint(600, 1000),
            'sessionsWon': random.randint(50, 100),
            'shinyPokemonCaught': round(caught / 64),
            'shinyPokemonHatched': random.randint(70, 150),
            'shinyPokemonSeen': random.randint(50, 150),
            'subLegendaryPokemonCaught': random.randint(10, 100),
            'subLegendaryPokemonHatched': random.randint(10, 100),
            'subLegendaryPokemonSeen': random.randint(10, 100),
            'trainersDefeated': random.randint(100, 200)
        }

        choices = {
            'random': 'Randomize all values',
            'manual': 'Manually enter values for a single attribute',
            'loop': 'Manually enter values for all attributes in a loop'
        }

        action = self.fh_getChoiceInput('Choose which attribute to modify. You can type either ID or Name.', choices, renderMenu=True, zeroCancel=True)

        changed = False
        changedItems = []
        
        if action == 'random':
            for key, value in keysToUpdate.items():
                changedItems.append(f"{key}: {value}")
                gameData["gameStats"][key] = value
                changed = True

        elif action == 'manual':
            changed = False
            optionList = {str(index + 1): key for index, key in enumerate(keysToUpdate.keys())}
            nameToKey = {key.lower(): key for key in keysToUpdate.keys()}

            menuDisplay = "\n".join([f"{index}: {key} ({gameData['gameStats'].get(key, 0)})" for index, key in optionList.items()])
            cFormatter.print(Color.INFO, menuDisplay)
            while True:
                try:
                    inputValue = self.fh_getCompleterInput(
                        'Choose attribute to edit:',
                        {**optionList, **nameToKey},
                        softCancel=True
                    ).lower()

                    promptMessage = f'Enter new value for {inputValue} (Current: {gameData["gameStats"].get(inputValue, 0)}): '
                    newValue = self.fh_getIntegerInput(promptMessage, 0, 999999, softCancel=True)

                    gameData["gameStats"][inputValue] = newValue
                    changedItems.append(f"{inputValue}: {newValue}")
                    changed = True
                    cFormatter.print(Color.DEBUG, f'{inputValue} queued for update.')
                except OperationSoftCancel:
                    break

        elif action == 'loop':
            changed = False
            for key in keysToUpdate:
                try:
                    while True:
                        promptMessage = f'Enter new value for {key} ({gameData["gameStats"].get(key, 0)}): '
                        newValue = self.fh_getIntegerInput(promptMessage, 0, 999999, softCancel=True)
                        gameData["gameStats"][key] = newValue
                        changedItems.append(f"{key}: {newValue}")
                        changed = True
                        break
                except OperationSoftCancel:
                    break

        if changed:
            self.__writeJSONData(gameData, 'trainer.json')
            cFormatter.print(Color.YELLOW, 'Changes saved:')
            for item in changedItems:
                cFormatter.print(Color.INFO, item)
            raise OperationSuccessful('Successfully written Account Stats.')
        else:
            cFormatter.print(Color.YELLOW, 'No changes made.')

    @handle_operation_exceptions
    def f_editHatchWaves(self) -> None:
        """
        Edits the hatch waves for eggs in the trainer's inventory using helper functions for input validation.

        Raises:
        - Exception: If any error occurs during the process due to the decorator.
        - OperationCancel(), OperationSoftCancel(), ValueError() depending on input due to the helper.
        - OperationSuccessful(f'Set hatch duration of your eggs to {hatchWaves}')

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads trainer data from 'trainer.json'.
        2. Checks if there are any eggs in the trainer's inventory.
        3. Allows the player to input the number of waves after which eggs should hatch using validated input.
        4. Updates the hatch waves attribute for all eggs in the trainer's inventory.
        5. Writes updated trainer data to 'trainer.json'.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.f_editHatchWaves()
        """
        trainerData = self.__loadDataFromJSON('trainer.json')

        if 'eggs' in trainerData and trainerData['eggs']:
            minBound = 0
            maxBound = 99
            eggAmount = len(trainerData['eggs'])
            prompt = f'You currently have [{eggAmount}] eggs - after how many waves should they hatch?'
            hatchWaves = self.fh_getIntegerInput(prompt, minBound, maxBound, zeroCancel=True)

            for egg in trainerData['eggs']:
                egg["hatchWaves"] = hatchWaves

            # Write updated trainer_data to 'trainer.json'
            self.__writeJSONData(trainerData, 'trainer.json')
            raise OperationSuccessful(f'Set hatch duration of your eggs to {hatchWaves}')
        else:
            cFormatter.print(Color.GREEN, 'You have no eggs to hatch.')
            return

    @handle_operation_exceptions
    def f_submenuItemEditor(self):
        from modules import ModifierEditor
        edit = ModifierEditor()
        edit.m_itemMenuPresent(self.slot)

    @handle_operation_exceptions
    def f_changeSaveSlot(self):
        while True:
            newSlot = self.fh_getIntegerInput(
                'Select a slot: ', 1, 5,
                zeroCancel=True
            )
            filename = f'slot_{newSlot}.json'
            if int(self.slot) == int(newSlot):
                cFormatter.print(Color.ERROR, f'Slot {filename} already loaded.')
            else:
                if self.editOffline:
                    # Construct the filename
                    
                    if os.path.exists(filename):
                        self.slot = newSlot
                        raise OperationSuccessful(f'Changed slot to {newSlot}')
                    else:
                        cFormatter.print(Color.ERROR, f'File {filename} does not exist. Please select another slot.')
                else:
                    self.get_trainer_data(newSlot)

    @staticmethod
    def fh_getChoiceInput(promptMesage: str, choices: dict, renderMenu: bool = False, zeroCancel: bool=False, softCancel:bool = False) -> str:
        """
        Args:
        - promptMesage (str): The prompt message to display.
        - choices (dict): The dictionary containing choice options.
        - renderMenu (bool): If True, render the menu with line breaks for readability.
        - zeroCancel (bool): If True, allow raise cancellation with '0' interrupting the operation and save.
        - softCancel (bool): If True, allow soft cancellation with '0' interrupting the operation but allow saving.

        Helper method to get a validated choice input from the user.

        Raises:
        - OperationCancel()
        - OperationSoftCancel()
        - ValueError()

        Returns:
        - str: The validated choice key.
        - or any Raise depending on setup.
        """
        if renderMenu:
            actions = "\n".join([f'{idx + 1}: {desc}' for idx, desc in enumerate(choices.values())])
            fullPrompt = f'{promptMesage}\n{actions}\nSelect a option (0: Cancel): '
        else:
            actions = " | ".join([f'{idx + 1}: {desc}' for idx, desc in enumerate(choices.values())])
            if zeroCancel or softCancel:
                fullPrompt = f'{promptMesage} (0: Cancel | {actions}): '
            else:
                fullPrompt = f'{promptMesage} ({actions}): '

        while True:
            userInput = input(fullPrompt).strip()
            if userInput.lower() == 'exit' or userInput.lower() == 'cancel':
                raise OperationCancel()
            if userInput == '0':
                if zeroCancel:
                    raise OperationCancel()
                if softCancel:
                    raise OperationSoftCancel()
                
            # If no cancel or skip is requested
            if userInput.isdigit():
                idx = int(userInput) - 1
                if 0 <= idx < len(choices):
                    return list(choices.keys())[idx]
                
            raise ValueError(f'{userInput}')

    @staticmethod
    def fh_getIntegerInput(promptMessage: str, minBound: int, maxBound: int, zeroCancel: bool=False, softCancel: bool=False, allowSkip: bool=False) -> int:
        """
        Args:
        - prompt (str): The prompt message to display.
        - minBound (int): The minimum valid value.
        - maxBound (int): The maximum valid value.
        - zeroCancel (bool): If True, allow raise cancellation with '0' interrupting the operation and save.
        - softCancel (bool): If True, allow soft cancellation with '0' interrupting the operation but allow saving.
        - allowSkip (bool): If True, returns 'skip' 
        Helper method to get a validated integer input from the user.


        Raises:
        - OperationCancel()
        - OperationSoftCancel()
        - ValueError()
            
        Returns:
        - int: The validated integer input.
        - or any Raise depending on setup.
        """
        if zeroCancel or softCancel or allowSkip:
            minBound = 0
            fullPrompt = f'{promptMessage} (0: Cancel | 1 - {maxBound} | "skip"): ' if allowSkip else f'{promptMessage} (0: Cancel | 1 - {maxBound}): '
        else:
            fullPrompt = f'{promptMessage} ({minBound} - {maxBound}): '

        while True:
            userInput = input(fullPrompt).strip()
            if userInput.lower() == 'exit' or userInput.lower() == 'cancel':
                raise OperationCancel()
            if userInput == '0':
                if zeroCancel:
                    raise OperationCancel()
                elif softCancel:
                    raise OperationSoftCancel()
            if allowSkip and userInput.lower() == 'skip':
                return 'skip'
            
            # If no cancel or skip is requested
            if userInput.isdigit():
                value = int(userInput)
                if minBound <= value <= maxBound:
                    return str(value)
                
            raise ValueError(f'{userInput}')

    @staticmethod
    def fh_getCompleterInput(promptMessage: str, choices: dict, zeroCancel: bool = False, softCancel: bool = False, allowSkip: bool = False) -> str:
        """
        Args:
        - prompt_message (str): The prompt message to display.
        - choices (dict): A dictionary mapping input choices to their corresponding values.
        - zeroCancel (bool): If True, allow raise cancellation with '0' interrupting the operation and save.
        - softCancel (bool): If True, allow soft cancellation with '0' interrupting the operation but allow saving.

        Helper method to get input from the user with auto-completion support.

        Raises:
        - OperationSoftCancel()
        - OperationCancel()
        - ValueError()

        Returns:
        - str: The value corresponding to the validated input choice, or raises OperationCancel if the user cancels.
        - or any Raise depending on setup.
        """
        fullPrompt = f'{promptMessage}: '
        if zeroCancel or softCancel:
            fullPrompt = f'{promptMessage} (0: Cancel): '

        # Create a WordCompleter from the keys of choices dictionary
        completer = WordCompleter(choices.keys(), ignore_case=True)

        while True:
            userInput = prompt(fullPrompt, completer=completer).strip()  # Ensure prompt is the correct callable

            if userInput.lower() == 'exit' or userInput.lower() == 'cancel':
                raise OperationCancel()
            if userInput == '0':
                if softCancel:
                    raise OperationSoftCancel()
                if zeroCancel:
                    raise OperationCancel()
            if allowSkip and userInput.lower() == 'skip':
                return 'skip'
            
            ## Validate the input
            if userInput in choices:
                return choices[userInput]

            # Ensure inputValue is a string
            inputValue = str(userInput).strip().lower()

            if inputValue.isdigit():
                # Input is an ID
                enum_member = next((member for member in choices.values() if isinstance(member, Enum) and member.value == int(inputValue)), None)
            else:
                # Input is a name
                enum_member = next((member for member in choices.values() if isinstance(member, Enum) and member.name.lower() == inputValue), None)

            if enum_member is not None:
                return enum_member

            # If input is not valid
            raise ValueError(f'{userInput}')
        
    @handle_operation_exceptions
    def fh_printEnums(self, enum_type: str) -> None:
        """
        enums_mapping = {
            'pokedex': self.pokemon_id_by_name,
            'biomes': self.biomesByID,
            'moves': self.moves_by_id,
            'natures': self.natureData,
            'vouchers': self.vouchers_data,
            'natureSlot': self.natureSlot_data,
        }
        """
        enums_mapping = {
            'pokedex': self.pokemon_id_by_name,
            'biomes': self.biomesByID,
            'moves': self.moves_by_id,
            'natures': self.natureData,
            'vouchers': self.vouchers_data,
            'natureSlot': self.natureSlot_data,
        }

        if enum_type not in enums_mapping:
            raise ValueError(f"Invalid enum_type: {enum_type}. Valid types are: {', '.join(enums_mapping.keys())}")

        enums = enums_mapping[enum_type]
        formatted_enums = [f'{member.value}: {member.name}' for member in enums]
        cFormatter.print(Color.WHITE, '\n'.join(formatted_enums))

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

from modules import handle_error_response, HeaderGenerator, config
from utilities import Generator, EnumLoader, cFormatter, Color, Limiter, eggLogic

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

limiter = Limiter(lockout_period=40, timestamp_file='./data/extra.json')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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

    def __init__(self, session: requests.Session, auth_token: str, clientSessionId: str = None, driver: dict = None, useScripts: Optional[bool] = None) -> None:
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
        self.enum = EnumLoader()

        self.backup_dir = config.backups_directory
        self.data_dir = config.data_directory

        self.pokemon_id_by_name, self.biomes_by_id, self.moves_by_id, self.nature_data, self.vouchers_data, self.natureSlot_data = self.enum.convert_to_enums()

        try:
            with open(f'{self.data_dir}/extra.json') as f:
                self.extra_data = json.load(f)
            
            with open(f'{self.data_dir}/passive.json') as f:
                self.passive_data = json.load(f)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Something on inital data generation failed. {e}', isLogging=True)
        
        self.__dump_data()

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
            if not self.slot:
                slot = int(input('Enter slot (1-5): '))
                self.slot = slot
                if slot > 5 or slot < 1:
                    cFormatter.print(Color.INFO, 'Invalid input.')
                    return

            trainer_data = self.get_trainer_data()
            game_data = self.get_gamesave_data(slot)

            if game_data and trainer_data:
                self.create_backup()

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function __dump_data(): {e}', isLogging=True)

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
                        data = json.loads(response)
                        self.__write_data(data, 'trainer.json', False)
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
                    self.__write_data(data, 'trainer.json', False)
                    return data
                else:
                    return handle_error_response(response)
            except requests.RequestException as e:
                cFormatter.print(Color.DEBUG, f'Error fetching trainer data. Please restart the tool. \n {e}', isLogging=True)

    @limiter.lockout
    def get_gamesave_data(self, slot: int = 1) -> Optional[Dict[str, Any]]:
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
                        data = json.loads(response)
                        self.__write_data(data, f'slot_{slot}.json', False)
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
                    cFormatter.print(Color.GREEN, 'Successfully fetched data.')
                    data = response.json()
                    self.__write_data(data, f'slot_{slot}.json', False)
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
            exit(0)
        except Exception as e:
            cFormatter.print(Color.WARNING, f'Error logging out. {e}')

    def __write_data(self, data: Dict[str, Any], filename: str, showSuccess: bool = True) -> None:
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

    def __load_data(self, file_path: str) -> Dict[str, Any]:
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


    def create_backup(self) -> None:
        """
        Create a backup of JSON files.

        What it does:
        - Creates a backup of all JSON files in the current directory to `config.backups_directory`.
        - Uses a timestamped naming convention for backup files (`backup_{trainerid}_{timestamp}.json`).
        - Prints 'Backup created.' upon successful backup completion.

        :args: None
        :params: None

        Usage Example:
            instance.create_backup()

        Output Example:
            # Output: backup/backup_{trainerid}_{timestamp}.json
            # Backup created.

        Modules/Librarys used and for what purpose exactly in each function:
        - os: For directory creation and file handling operations.
        - json: For loading JSON data from files.
        - shutil: For copying files from the current directory to the backup directory.
        - datetime: For generating timestamps for backup file names.
        """

        backup_dir = 'backup'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        try:
            for file in os.listdir('.'):
                if file.endswith('.json'):
                    with open(file, 'r') as f:
                        data = json.load(f)
                    trainer_id = data.get('trainerId')
                    if trainer_id is not None:
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        base_filename = f'base_{trainer_id}.json'
                        base_filepath = os.path.join(backup_dir, base_filename)

                        if os.path.exists(base_filepath):
                            backup_filename = f'backup_{trainer_id}_{timestamp}.json'
                            backup_filepath = os.path.join(backup_dir, backup_filename)
                            shutil.copy(file, backup_filepath)
                        else:
                            shutil.copy(file, base_filepath)
                        cFormatter.print(Color.GREEN, 'Backup created.')
        except Exception as e:
            cFormatter.print(Color.WARNING, f'Error in function create_backup(): {e}')

    def restore_backup(self) -> None:
        """
        Restore a backup of JSON files and update the timestamp in trainer.json.

        What it does:
        - Restores a selected backup file (`backup_{trainerid}_{timestamp}.json`) to `trainer.json`.
        - Updates the timestamp in `trainer.json` with the current timestamp upon restoration.
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
            # Enter the number of the file you want to restore: 2
            # Data restored.

        Modules/Librarys used and for what purpose exactly in each function:
        - os: For directory listing and file handling operations.
        - re: For filtering and sorting backup files based on trainer ID patterns.
        - shutil: For copying files from the backup directory to `trainer.json`.
        - datetime: For generating timestamps and updating timestamps in `trainer.json`.
        """

        try:
            backup_dir = 'backup'
            files = os.listdir(backup_dir)

            # Filter and sort files that match trainerId
            trainer_id_pattern = f'_{self.trainerId}_'
            backup_files = sorted(
                (f for f in files if re.match(rf'(base|backup){trainer_id_pattern}\d{{8}}_\d{{6}}\.json', f)),
                key=lambda x: (re.findall(r'\d+', x)[0], re.findall(r'\d{8}_\d{6}', x)[0])
            )

            if not backup_files:
                cFormatter.print(Color.WARNING, 'No backup files found for your trainer ID.')
                return

            # Displaying sorted list with numbers
            for idx, file in enumerate(backup_files, 1):
                sidenote = '        <- Created on first edit' if file.startswith('base_') else ''
                print(f'{idx}: {file} {sidenote}')

            # Getting user's choice
            while True:
                try:
                    choice = int(input('Enter the number of the file you want to restore: '))
                    if 1 <= choice <= len(backup_files):
                        chosen_file = backup_files[choice - 1]
                        chosen_filepath = os.path.join(backup_dir, chosen_file)

                        # Determine the output filepath
                        parent_dir = os.path.abspath(os.path.join(backup_dir, os.pardir))
                        output_filepath = os.path.join(parent_dir, './trainer.json')

                        # Copy the chosen file to the output filepath
                        shutil.copyfile(chosen_filepath, output_filepath)

                        # Read the restored file
                        with open(output_filepath, 'r') as file:
                            data = json.load(file)

                        # Update the timestamp
                        current_timestamp = int(datetime.now().timestamp() * 1000)
                        data['timestamp'] = current_timestamp

                        # Write the updated data back to the file
                        with open(output_filepath, 'w') as file:
                            json.dump(data, file, indent=4)

                        cFormatter.print(Color.GREEN, 'Data restored and timestamp updated.')
                        break
                    else:
                        cFormatter.print(Color.WARNING, 'Invalid choice. Please enter a number within range.')
                except ValueError:
                    cFormatter.print(Color.GREEN, 'Invalid choice. Please enter a valid number.')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function restore_backup(): {e}', isLogging=True)

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
            if self.useScripts:
                response = self._make_request(url, method='POST', data=json.dumps(payload))
                cFormatter.print("That seemed to work! Refresh without cache (STRG+F5)")
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
        except ConnectionError as conn_err:
            cFormatter.print(Color.WARNING, f'Connection error occurred: {conn_err}', isLogging=True)
        except Timeout as timeout_err:
            cFormatter.print(Color.WARNING, f'Timeout error occurred: {timeout_err}', isLogging=True)
        except requests.exceptions.RequestException as e:
           cFormatter.print(Color.WARNING, f'Error occurred during request: {e}', isLogging=True)

    def unlock_all_starters(self) -> None:
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
            trainer_data: dict = self.__load_data('trainer.json')

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
                    'natureAttr': self.nature_data.UNLOCK_ALL.value if nature == 1 else None,
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

            self.__write_data(trainer_data, 'trainer.json')
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
            trainer_data: dict = self.__load_data('trainer.json')
            
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
            
            self.print_natures()

            nature_completer: WordCompleter = WordCompleter(self.nature_data.__members__.keys(), ignore_case=True)
            
            cFormatter.print(Color.BRIGHT_YELLOW, 'Write the name of the nature, it will recommend for auto-completion.')
            nature: str = prompt('What nature would you like?: ', completer=nature_completer)

            nature: int = self.nature_data[nature].value

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

            self.__write_data(trainer_data, 'trainer.json')
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
            trainer_data = self.__load_data('trainer.json')

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

            self.__write_data(trainer_data, 'trainer.json')
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

            game_data = self.__load_data(filename)

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

            cFormatter.print_separators(65, '-', Color.WHITE)
            cFormatter.print(Color.WHITE, '\n'.join(options))
            cFormatter.print_separators(65, '-', Color.WHITE)

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
                
                self.print_moves()

                move_completer: WordCompleter = WordCompleter(self.moves_by_id.__members__.keys(), ignore_case=True)
                
                cFormatter.print(Color.INFO, 'Write the name of the move, it will recommend for auto completion.')
                move: str = prompt('What move would you like?: ', completer=move_completer)

                move: int = int(self.moves_by_id[move].value)
            
                game_data['party'][party_num]['moveset'][move_slot]['moveId'] = move
            else:
                self.print_natureSlot()

                natureSlot_completer: WordCompleter = WordCompleter(self.natureSlot_data.__members__.keys(), ignore_case=True)
                cFormatter.print(Color.INFO, 'Write the name of the nature, it will recommend for auto-completion.')
                natureSlot: str = prompt('What nature would you like?: ', completer=natureSlot_completer)

                natureSlot: int = int(self.natureSlot_data[natureSlot].value)
            
                game_data['party'][party_num]['nature'] = natureSlot

            self.__write_data(game_data, filename)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_pokemon_party(): {e}', isLogging=True)

    def unlock_all_gamemodes(self) -> None:
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
            trainer_data = self.__load_data('trainer.json')

            unlocked_modes = trainer_data.get('unlocks', {})
            if not unlocked_modes:
                cFormatter.print(Color.INFO, 'Unable to find data entry: unlocks')
                return

            for mode in unlocked_modes:
                unlocked_modes[mode] = True

            self.__write_data(trainer_data, 'trainer.json')
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function unlock_all_gamemodes(): {e}', isLogging=True)

    def unlock_all_achievements(self) -> None:
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
            trainer_data = self.__load_data('trainer.json')

            current_time_ms = int(time.time() * 1000) 
            min_time_ms = current_time_ms - 3600 * 1000  

            achievements = self.extra_data['achievements']
            trainer_data['achvUnlocks'] = {
                achievement: random.randint(min_time_ms, current_time_ms)
                for achievement in achievements
            }

            self.__write_data(trainer_data, 'trainer.json')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function unlock_all_achievements(): {e}', isLogging=True)

    def edit_vouchers(self) -> None:
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
            trainer_data = self.__load_data('trainer.json')

            current_time_ms = int(time.time() * 1000) 
            min_time_ms = current_time_ms - 3600 * 1000  
            
            self.print_vouchers()

            choice: int = int(input('Do you want to unlock all vouchers or unlock a specific voucher? (1: All | 2: Specific): '))

            if (choice < 1) or (choice > 2):
                cFormatter.print(Color.INFO, 'Invalid command.')
                return
            elif choice == 1:
                voucher_unlocks = {}
                for voucher in self.vouchers_data.__members__:
                    random_time = min_time_ms + random.randint(0, current_time_ms - min_time_ms)
                    voucher_unlocks[voucher] = random_time
                trainer_data['voucherUnlocks'] = voucher_unlocks
            else:
                vouchers_completer: WordCompleter = WordCompleter(self.vouchers_data.__members__.keys(), ignore_case=True)
                cFormatter.print(Color.INFO, 'Write the name of the voucher, it will recommend for auto-completion.')
            
                vouchers: str = prompt('What voucher would you like?: ', completer=vouchers_completer)

                if 'voucherUnlocks' in trainer_data and vouchers in trainer_data['voucherUnlocks']:
                    random_time = min_time_ms + random.randint(0, current_time_ms - min_time_ms)
                    trainer_data['voucherUnlocks'][vouchers] = random_time
                else:
                    random_time = min_time_ms + random.randint(0, current_time_ms - min_time_ms)
                    trainer_data['voucherUnlocks'][vouchers] = random_time

            self.__write_data(trainer_data, 'trainer.json')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_vouchers(): {e}', isLogging=True)

    def print_pokedex(self) -> None:
        """
        Prints all Pokemon available in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Retrieves Pokemon data.
        2. Prints out the list of Pokemon available in the game.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.print_pokedex()

        """
        try:
            pokemons = [f'{member.value}: {member.name}' for member in self.pokemon_id_by_name]
            cFormatter.print(Color.WHITE, '\n'.join(pokemons))
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function print_pokedex(): {e}', isLogging=True)

    def print_biomes(self) -> None:
        """
        Prints all biomes available in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Retrieves biome data.
        2. Prints out the list of biomes available in the game.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.print_biomes()

        """
        try:
            biomes = [f'{member.value}: {member.name}' for member in self.biomes_by_id]
            cFormatter.print(Color.WHITE, '\n'.join(biomes))
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function print_biomes(): {e}', isLogging=True)

    def print_moves(self) -> None:
        """
        Prints all moves available in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Retrieves move data.
        2. Prints out the list of moves available in the game.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.print_moves()

        """
        try:
            moves = [f'{member.value}: {member.name}' for member in self.moves_by_id]
            cFormatter.print(Color.WHITE, '\n'.join(moves))
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function print_moves(): {e}', isLogging=True)

    def print_natures(self) -> None:
        """
        Prints all natures available in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Retrieves nature data.
        2. Prints out the list of natures available in the game.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.print_natures()

        """
        try:
            natures = [f'{member.value}: {member.name}' for member in self.nature_data]
            cFormatter.print(Color.WHITE, '\n'.join(natures))
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function print_natures(): {e}', isLogging=True)
    
    def print_vouchers(self) -> None:
        """
        Prints all vouchers available in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Retrieves voucher data.
        2. Prints out the list of vouchers available in the game.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.print_vouchers()

        """
        try:
            vouchers = [f'{member.value}: {member.name}' for member in self.vouchers_data]
            cFormatter.print(Color.WHITE, '\n'.join(vouchers))
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function print_vouchers(): {e}', isLogging=True)

    def print_natureSlot(self) -> None:
        """
        Prints all natureSlot IDs available in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Retrieves natureSlot data.
        2. Prints out the list of natureSlot IDs available in the game.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.print_natureSlot()

        """
        try:
            natureSlot = [f'{member.value}: {member.name}' for member in self.natureSlot_data]
            cFormatter.print(Color.WHITE, '\n'.join(natureSlot))
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function print_natureSlot(): {e}', isLogging=True)

    def add_candies(self, dexId: Optional[str] = None) -> None:
        """
        Adds candies to a Pokémon.

        Args:
        - dexId (str, optional): The ID of the Pokémon. Defaults to None.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads trainer data.
        2. Allows the player to specify a Pokémon by name or ID (optional).
        3. Allows the player to input the number of candies to add to the Pokémon.
        4. Updates the game data with the new candy count for the Pokémon.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.add_candies('pikachu')

        """
        try:
            trainer_data = self.__load_data('trainer.json')
            
            if not dexId:
                pokemon_completer: WordCompleter = WordCompleter(self.pokemon_id_by_name.__members__.keys(), ignore_case=True)

                cFormatter.print(Color.INFO, 'Write the name of the pokemon it will recommend for auto-completion.')
                dexId: str = prompt('Enter Pokemon (Name / ID): ', completer=pokemon_completer)
            
                try:
                    dexId: str = self.pokemon_id_by_name[dexId.lower()].value
                except KeyError:
                    cFormatter.print(Color.INFO, f'No Pokemon with Name: {dexId}')
                    return
                
            candies = int(input('How many candies you want on your pokemon: '))
            trainer_data['starterData'][dexId]['candyCount'] = candies

            self.__write_data(trainer_data, 'trainer.json')
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function add_candies(): {e}', isLogging=True)

    def edit_biome(self) -> None:
        """
        Edits the biome of the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads game data for the current slot.
        2. Allows the player to choose a biome by name.
        3. Updates the game data with the chosen biome.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_biome()

        """
        try:
            game_data = self.__load_data(f'slot_{self.slot}.json')
            self.print_biomes()
            biome_completer: WordCompleter = WordCompleter(self.biomes_by_id.__members__.keys(), ignore_case=True)
            cFormatter.print(Color.INFO, 'Write the name of the biome, it will recommend for auto-completion.')

            biome: str = prompt('What biome would you like?: ', completer=biome_completer)
            biome: int = int(self.biomes_by_id[biome].value)
            game_data['arena']['biome'] = biome
            self.__write_data(game_data, f'slot_{self.slot}.json')
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_biome(): {e}', isLogging=True)

    def edit_pokeballs(self) -> None:
        """
        Edits the number of pokeballs in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads game data for the current slot.
        2. Allows the player to input the number of each type of pokeball.
        3. Updates the game data with the new counts for each type of pokeball.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_pokeballs()

        """
        try:
            game_data = self.__load_data(f'slot_{self.slot}.json')

            if game_data['gameMode'] == 3:
                cFormatter.print(Color.CRITICAL, 'Cannot edit this property on daily runs!')
                return

            choice = int(input('How many pokeballs do you want?: '))
            game_data['pokeballCounts']['0'] = choice

            choice = int(input('How many great balls do you want?: '))
            game_data['pokeballCounts']['1'] = choice

            choice = int(input('How many ultra balls do you want?: '))
            game_data['pokeballCounts']['2'] = choice

            choice = int(input('How many rogue balls do you want?: '))
            game_data['pokeballCounts']['3'] = choice

            choice = int(input('How many master balls do you want?: '))
            game_data['pokeballCounts']['4'] = choice

            self.__write_data(game_data, f'slot_{self.slot}.json')
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_pokeballs(): {e}', isLogging=True)

    def edit_money(self) -> None:
        """
        Edits the amount of Poke-Dollars in the game.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads game data for the current slot.
        2. Allows the player to input the amount of Poke-Dollars they want.
        3. Updates the game data with the new amount of Poke-Dollars.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_money()

        """
        try:
            game_data = self.__load_data(f'slot_{self.slot}.json')

            if game_data['gameMode'] == 3:
                cFormatter.print(Color.CRITICAL, 'Cannot edit this property on daily runs!')
                return

            choice = int(input('How many Poke-Dollars do you want?: '))
            game_data['money'] = choice
            self.__write_data(game_data, f'slot_{self.slot}.json')
        
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_money(): {e}', isLogging=True)

    def generate_eggs(self) -> None:
        """
        Generates eggs for the player.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.
        - eggLogic: Module or class responsible for generating eggs, assumed to be imported or available.

        Workflow:
        1. Loads trainer data.
        2. Allows the player to specify attributes for the eggs (count, tier, gacha type, hatch waves).
        3. Generates the specified number of eggs with the specified attributes.
        4. Adds the generated eggs to the player's inventory.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.generate_eggs()

        """
        try:
            trainer_data = self.__load_data('trainer.json')

            if trainer_data['eggs'] is not None:
                egg_len = len(trainer_data['eggs'])
            else:
                trainer_data['eggs'] = []
                egg_len = len(trainer_data['eggs'])
            
            if egg_len >= 75:
                replace_or_add = input(
                    'You have max number of eggs, replace eggs? (0: Cancel, 1: Replace): '
                )
                if replace_or_add == '2':
                    replace_or_add = '1'
            else:
                replace_or_add = input(
                    f'You have [{egg_len}] eggs, add or replace eggs? (0: Cancel, 1: Replace, 2: Add): '
                )
                
            if replace_or_add not in ['1', '2']:
                raise ValueError('Invalid replace_or_add selected!')
                
            max_count = 75 - egg_len if replace_or_add == '2' else 75
            
            count = int(
                input(f'How many eggs do you want to have? (0 - {max_count})(number): ')
            )
            tier = input(
                'What tier should the eggs have? (1: Common, 2: Rare, 3: Epic, 4: Legendary, 5: Manaphy): '
            )
            # Map tier to string
            tier_map = {
                '1': 'COMMON',
                '2': 'RARE',
                '3': 'EPIC',
                '4': 'LEGENDARY',
                '5': 'MANAPHY'
            }
            if tier not in tier_map:
                raise ValueError('Invalid tier selected!')
            tier = tier_map[tier]
            
            gacha_type = input(
                'What gacha type do you want to have? (1: Move, 2: Legendary, 3: Shiny): '
            )
            # Map gacha type to string
            gacha_map = {
                '1': 'MOVE',
                '2': 'LEGENDARY',
                '3': 'SHINY'
            }
            if gacha_type not in gacha_map:
                raise ValueError('Invalid gacha_type selected!')
            gacha_type = gacha_map[gacha_type]
            
            hatch_waves = int(
                input('After how many waves should they hatch? (0-100)(number): ')
            )

            new_eggs = eggLogic.generate_eggs(tier, gacha_type, hatch_waves, count)  # noqa: F405

            if replace_or_add == '1':
                trainer_data['eggs'] = new_eggs
            elif replace_or_add == '2':
                trainer_data['eggs'].extend(new_eggs)
            
            cFormatter.print(Color.GREEN, f'[{count}] eggs generated successfully.')
            self.__write_data(trainer_data, 'trainer.json')
            

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function generate_eggs(): {e}', isLogging=True)

    def edit_account_stats(self) -> None:
        """
        Edits the statistics of the player's account.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads trainer data from 'trainer.json'.
        2. Allows the player to input various statistics related to their gameplay.
        3. Updates the trainer data with the new statistics.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_account_stats()

        """
        try:
            trainer_data = self.__load_data('trainer.json')
            
            # Input for various gameplay statistics
            battles: int = int(input('How many battles: '))
            classicSessionsPlayed: int = int(input('How many classicSessionsPlayed: '))
            dailyRunSessionPlayed: int = int(input('How many dailyRunSessionPlayed: '))
            dailyRunSessionWon: int = int(input('How many dailyRunSessionWon: '))
            eggsPulled: int = int(input('How many eggsPulled: '))
            endlessSessionsPlayed: int = int(input('How many endlessSessionsPlayed: '))
            epicEggsPulled: int = int(input('How many epicEggsPulled: '))
            highestDamage: int = int(input('How many highestDamage: '))
            highestEndlessWave: int = int(input('How many highestEndlessWave: '))
            highestHeal: int = int(input('How many highestHeal: '))
            highestLevel: int = int(input('How many highestLevel: '))
            highestMoney: int = int(input('How many highestMoney: '))
            legendaryEggsPulled: int = int(input('How many legendaryEggsPulled: '))
            legendaryPokemonCaught: int = int(input('How many legendaryPokemonCaught: '))
            legendaryPokemonHatched: int = int(input('How many legendaryPokemonHatched: '))
            legendaryPokemonSeen: int = int(input('How many legendaryPokemonSeen: '))
            manaphyEggsPulled: int = int(input('How many manaphyEggsPulled: '))
            mythicalPokemonCaught: int = int(input('How many mythicalPokemonCaught: '))
            mythicalPokemonHatched: int = int(input('How many mythicalPokemonHatched: '))
            mythicalPokemonSeen: int = int(input('How many mythicalPokemonSeen: '))
            playTime: int = int(input('How much playtime in hours: '))
            pokemonCaught: int = int(input('How many pokemonCaught: '))
            pokemonDefeated: int = int(input('How many pokemonDefeated: '))
            pokemonFused: int = int(input('How many pokemonFused: '))
            pokemonHatched: int = int(input('How many pokemonHatched: '))
            pokemonSeen: int = int(input('How many pokemonSeen: '))
            rareEggsPulled: int = int(input('How many rareEggsPulled: '))
            ribbonsOwned: int = int(input('How many ribbonsOwned: '))
            sessionsWon: int = int(input('How many sessionsWon: '))
            shinyPokemonCaught: int = int(input('How many shinyPokemonCaught: '))
            shinyPokemonHatched: int = int(input('How many shinyPokemonHatched: '))
            shinyPokemonSeen: int = int(input('How many shinyPokemonSeen: '))
            subLegendaryPokemonCaught: int = int(input('How many subLegendaryPokemonCaught: '))
            subLegendaryPokemonHatched: int = int(input('How many subLegendaryPokemonHatched: '))
            subLegendaryPokemonSeen: int = int(input('How many subLegendaryPokemonSeen: '))
            trainersDefeated: int = int(input('How many trainersDefeated: '))

            # Update gameStats in trainer_data
            trainer_data['gameStats'] = {
                'battles': battles,
                'classicSessionsPlayed': classicSessionsPlayed,
                'dailyRunSessionsPlayed': dailyRunSessionPlayed,
                'dailyRunSessionsWon': dailyRunSessionWon,
                'eggsPulled': eggsPulled,
                'endlessSessionsPlayed': endlessSessionsPlayed,
                'epicEggsPulled': epicEggsPulled,
                'highestDamage': highestDamage,
                'highestEndlessWave': highestEndlessWave,
                'highestHeal': highestHeal,
                'highestLevel': highestLevel,
                'highestMoney': highestMoney,
                'legendaryEggsPulled': legendaryEggsPulled,
                'legendaryPokemonCaught': legendaryPokemonCaught,
                'legendaryPokemonHatched': legendaryPokemonHatched,
                'legendaryPokemonSeen': legendaryPokemonSeen,
                'manaphyEggsPulled': manaphyEggsPulled,
                'mythicalPokemonCaught': mythicalPokemonCaught,
                'mythicalPokemonHatched': mythicalPokemonHatched,
                'mythicalPokemonSeen': mythicalPokemonSeen,
                'playTime': playTime * 3600,  # Convert hours to seconds
                'pokemonCaught': pokemonCaught,
                'pokemonDefeated': pokemonDefeated,
                'pokemonFused': pokemonFused,
                'pokemonHatched': pokemonHatched,
                'pokemonSeen': pokemonSeen,
                'rareEggsPulled': rareEggsPulled,
                'ribbonsOwned': ribbonsOwned,
                'sessionsWon': sessionsWon,
                'shinyPokemonCaught': shinyPokemonCaught,
                'shinyPokemonHatched': shinyPokemonHatched,
                'shinyPokemonSeen': shinyPokemonSeen,
                'subLegendaryPokemonCaught': subLegendaryPokemonCaught,
                'subLegendaryPokemonHatched': subLegendaryPokemonHatched,
                'subLegendaryPokemonSeen': subLegendaryPokemonSeen,
                'trainersDefeated': trainersDefeated,
            }

            # Write updated trainer_data to 'trainer.json'
            self.__write_data(trainer_data, 'trainer.json')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_account_stats(): {e}', isLogging=True)


    def unlock_all_features(self) -> None:
        """
        Maximizes the statistics and attributes of the player's account.

        Raises:
        - None

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.
        - random: Standard library for generating random numbers.

        Workflow:
        1. Calls methods to unlock all game modes, achievements, vouchers, and starters.
        2. Generates random statistics for various gameplay attributes and updates the trainer data accordingly.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.unlock_all_features()

        """
        try:
            self.unlock_all_gamemodes()
            self.unlock_all_achievements()
            self.edit_vouchers()
            self.unlock_all_starters()

            trainer_data = self.__load_data('trainer.json')
        
            total_caught = 0
            total_seen = 0
            for entry in trainer_data['dexData'].keys():
                caught = random.randint(500, 1000)
                seen = random.randint(500, 1000)
                hatched = random.randint(500, 1000)
                total_caught += caught
                total_seen += seen
                randIv: List[int] = random.sample(range(20, 30), 6)

                trainer_data['dexData'][entry] = {
                    'seenAttr': random.randint(500, 5000),
                    'caughtAttr': self.__MAX_BIG_INT,
                    'natureAttr': self.nature_data.UNLOCK_ALL.value,
                    'seenCount': seen,
                    'caughtCount': caught,
                    'hatchedCount': hatched,
                    'ivs': randIv
                }

            trainer_data['gameStats'] = {
                'battles': total_caught + random.randint(1, total_caught),
                'classicSessionsPlayed': random.randint(2500, 10000),
                'dailyRunSessionsPlayed': random.randint(2500, 10000),
                'dailyRunSessionsWon': random.randint(50, 150),
                'eggsPulled': random.randint(100, 300),
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
                'playTime': random.randint(5000, 10000) * 100,
                'pokemonCaught': total_caught,
                'pokemonDefeated': random.randint(2500, 10000),
                'pokemonFused': random.randint(50, 150),
                'pokemonHatched': random.randint(2500, 10000),
                'pokemonSeen': total_seen,
                'rareEggsPulled': random.randint(150, 250),
                'ribbonsOwned': random.randint(600, 1000),
                'sessionsWon': random.randint(50, 100),
                'shinyPokemonCaught': len(list(trainer_data['dexData'])) * 2,
                'shinyPokemonHatched': random.randint(70, 150),
                'shinyPokemonSeen': random.randint(50, 150),
                'subLegendaryPokemonCaught': random.randint(10, 100),
                'subLegendaryPokemonHatched': random.randint(10, 100),
                'subLegendaryPokemonSeen': random.randint(10, 100),
                'trainersDefeated': random.randint(100, 200),
            }

            self.__write_data(trainer_data, 'trainer.json')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function unlock_all_features(): {e}', isLogging=True)
  
    def edit_hatchWaves(self) -> None:
        """
        Edits the hatch waves for eggs in the trainer's inventory.

        Raises:
        - Exception: If any error occurs during the process.

        Modules Used:
        - .cFormatter: For printing formatted messages to the console, including colorized output.

        Workflow:
        1. Loads trainer data from 'trainer.json'.
        2. Checks if there are any eggs in the trainer's inventory.
        3. Allows the player to input the number of waves after which eggs should hatch.
        4. Updates the hatch waves attribute for all eggs in the trainer's inventory.
        5. Writes updated trainer data to 'trainer.json'.

        Usage Example:
            >>> example_instance = ExampleClass()
            >>> example_instance.edit_hatchWaves()

        """
        try:
            trainer_data = self.__load_data('trainer.json')

            if trainer_data['eggs'] is not None:
                egg_len = len(trainer_data['eggs'])
                hatch_waves = int(input(
                    f'You have a total of [{egg_len}] eggs - after how many waves should they hatch?: '
                ))
                
                for egg in trainer_data['eggs']:
                    egg['hatchWaves'] = hatch_waves

                # Write updated trainer_data to 'trainer.json'
                self.__write_data(trainer_data, 'trainer.json')
                
            else:
                cFormatter.print(Color.GREEN, 'You have no eggs to hatch.')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_hatchWaves(): {e}', isLogging=True)
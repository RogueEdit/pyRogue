# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 06.06.2024 

import requests
import json
import random
import os
import shutil
import brotli
import time
from typing import Dict, Any, Optional, List
import logging
from colorama import init, Fore, Style
from time import sleep
import datetime
import re
from modules.loginLogic import handle_error_response
import modules.config

from utilities.generator import Generator
from utilities.enumLoader import EnumLoader
from utilities.cFormatter import cFormatter, Color
from utilities.limiter import Limiter
from modules.loginLogic import HeaderGenerator

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from utilities.eggLogic import *
import string

from user_agents import parse
limiter = Limiter(lockout_period=120, timestamp_file='./data/extra.json')
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)


class Rogue:
    """
    A class to interact with the PokeRogue API for managing trainer and gamesave data.

    Attributes:
        TRAINER_DATA_URL (str): The URL to fetch trainer data from the API.
        GAMESAVE_SLOT_URL (str): The base URL to fetch gamesave data from a specific slot from the API.
        UPDATE_TRAINER_DATA_URL (str): The URL to update trainer data on the API.
        UPDATE_GAMESAVE_SLOT_URL (str): The base URL to update gamesave data for a specific slot on the API.
    """
    TRAINER_DATA_URL = 'https://api.pokerogue.net/savedata/system?clientSessionId='
    GAMESAVE_SLOT_URL = 'https://api.pokerogue.net/savedata/session?slot='
    UPDATE_TRAINER_DATA_URL = 'https://api.pokerogue.net/savedata/update?datatype=0'
    UPDATE_GAMESAVE_SLOT_URL = 'https://api.pokerogue.net/savedata/update?datatype=1&slot='
    UPDATE_ALL_URL = 'https://api.pokerogue.net/savedata/updateall'

    def __init__(self, session: requests.Session, auth_token: str, clientSessionId: str = None, headers: dict = None) -> None:
        self.slot = None
        self.session = session
        self.__MAX_BIG_INT = (2 ** 53) - 1
        self.auth_token = auth_token
        self.clientSessionId = clientSessionId
        self.headers = self._setup_headers()
        if not self.headers:
            raise ValueError("Failed to load headers.")

        # json generators
        self.generator = Generator()
        self.generator.generate()
        self.enum = EnumLoader()
        
        # wordcomplete
        self.pokemon_id_by_name, self.biomes_by_id, self.moves_by_id, self.nature_data, self.vouchers_data, self.natureSlot_data = self.enum.convert_to_enums()

        try:
            with open('./data/extra.json') as f:
                self.extra_data = json.load(f)
            
            with open('./data/passive.json') as f:
                self.passive_data = json.load(f)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Something on inital data generation failed. {e}', isLogging=True)
        
        self.__dump_data()

    def _setup_headers(self, headers = None) -> Dict[str, str]:
        """
        Generates random headers for the session.

        Returns:
            Dict[str, str]: The generated headers.
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

        Args:
            slot (int): The slot number (1-5). Defaults to 1.
        """
        try:
            if not self.slot:
                slot = int(input('Enter slot (1-5): '))
                self.slot = slot
                if slot > 5 or slot < 1:
                    cFormatter.print(Color.INFO, 'Invalid input.')
                    return

            trainer_data = self.get_trainer_data()
            cFormatter.print(Color.DEBUG, 'Sleeping 3 seconds to look more human before fetching saveslot-data.')
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
        """
        cFormatter.print(Color.INFO, 'Fetching trainer data...')
        try:
            response = self.session.get(f'{self.TRAINER_DATA_URL}{self.clientSessionId}', headers=self.headers)
            response.raise_for_status()
            if response.content:  # Check if the response content is not empty
                cFormatter.print(Color.GREEN, 'Successfully fetched data.')
                data = response.json()
                self.__write_data(data, 'trainer.json', False)
                return data
            else:
                return handle_error_response(response)
        except requests.RequestException as e:
            cFormatter.print(Color.DEBUG, f'Error fetching trainer data. Please restart the tool. \n {e}', isLogging=True)

    @limiter.lockout
    def get_gamesave_data(self, slot: int = 1):
        cFormatter.print(Color.INFO, f'Fetching data for Slot {slot}...')
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

    @limiter.lockout
    def __update_trainer_data(self, trainer_payload: dict) -> dict:
        """
        Update the trainer data on the server.

        Args:
            trainer_payload (dict): The payload containing trainer data to update.

        Returns:
            dict: JSON response from the server.
        """
        try:
            cFormatter.print(Color.INFO, 'Updating trainer data...')
            response = self.session.post(self.UPDATE_TRAINER_DATA_URL, headers=self.headers, json=trainer_payload)
            response.raise_for_status()
            if response.content:  # Check if the response content is not empty
                cFormatter.print(Color.GREEN, 'Succesfully updated data on the sever.')
                return response.json()
            else:
                return handle_error_response(response)
            
        except requests.RequestException as e:
            cFormatter.print(Color.BRIGHT_RED, 'Response 403 - Forbidden. We have no authoriazion to acces the resource.', isLogging=True)
            cFormatter.print(Color.BRIGHT_RED, 'Please report to our GitHub.', isLogging=True)

    @limiter.lockout
    def __update_gamesave_data(self, slot: int, gamedata_payload: Dict[str, any], url_ext: str) -> Dict[str, any]:
        """
        Update the gamesave data on the server.

        Args:
            slot (int): The slot number to update.
            gamedata_payload (Dict[str, any]): The payload containing game save data to update.
            url_ext (str): Additional URL parameters.

        Returns:
            Dict[str, any]: JSON response from the server.
        """
        try:
            cFormatter.print(Color.INFO, f'Updating gamesave data for slot {slot}...')
            response = self.session.post(
                f'{self.UPDATE_GAMESAVE_SLOT_URL}{slot - 1}{url_ext}', headers=self.headers, json=gamedata_payload)
            response.raise_for_status()
            if response.content:  # Check if the response content is not empty
                cFormatter.print(Color.GREEN, f'{response.json()} - That worked! Dont forget to clear your browser cache.')
            else:
                return handle_error_response(response)
            
        except requests.RequestException as e:
            # This might be TypeErrors not sure since httpreponse might be invalid here
            cFormatter.print(Color.BRIGHT_RED, 'Response 403 - Forbidden. We have no authoriazion to acces the resource.', isLogging=True)
            cFormatter.print(Color.BRIGHT_RED, 'Please report to our GitHub.', isLogging=True)
            return 
        sleep(1)

    def update_all(self) -> None:
        """
        Update all data to the server.
        """
        try:
            if self.slot is None or self.slot > 5 or self.slot < 1:
                cFormatter.print(Color.RED, 'Invalid slot number chosen.')
                return
            
            if 'trainer.json' not in os.listdir():
                cFormatter.print(Color.RED, 'Your gamefile trainer.json (Your game data) file not found')
                return
            
            trainer_data = self.__load_data('trainer.json')

            filename = f'slot_{self.slot}.json'
            if filename not in os.listdir():
                cFormatter.print(Color.RED, f'{filename} not found')
                return
            
            game_data = self.__load_data(filename)

            trainer_id, trainer_secretId = trainer_data['trainerId'], trainer_data['secretId']
            url_ext = f'&trainerId={trainer_id}&secretId={trainer_secretId}'

            self.__update_trainer_data(trainer_data)
            cFormatter.print(Color.DEBUG, 'Sleeping 3 seconds to look more human before saving saveslot-data.')
            sleep(3)
            self.__update_gamesave_data(self.slot, game_data, url_ext)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function update_all(): {e}', isLogging=True)

    def __write_data(self, data: Dict[str, any], filename: str, showSuccess: bool = True) -> None:
        """
        Write data to a JSON file.

        Args:
            data (Dict[str, any]): The data to write.
            filename (str): The name of the file.

        Example:
            # Assuming data is a dictionary and filename is a string.
            __write_data(data, 'trainer.json')
            # Output: -> writes into trainer.json
            # Written to local data. Do not forget to apply to server when done!
        """
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
                if showSuccess:
                    cFormatter.print(Color.BRIGHT_GREEN, 'Written to local data. Do not forget to apply to server when done!')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error .__writing_data(): {e}', isLogging=True)


    def __load_data(self, file_path: str) -> Dict[str, Any]:
            """"
            Load data from a specified file path.

            Args:
                file_path (str): Path to the file to be loaded.

            Returns:
                dict: Loaded data.

            Example:
                # Assuming file_path is a valid file path.
                __load_data('trainer.json')
                # Output:
                # Loaded data as a dictionary.

            Raises:
                Exception: If any error occurs during the process.
            """
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                cFormatter.print(Color.CRITICAL, f'Error in function .__load_data(): {e}', isLogging=True)

    def create_backup(self) -> None:
        """
        Create a backup of JSON files.

        Example:
            create_backup()
            # Output: backup/backup_{trainerid}_{timestamp}.json
            # Backup created.

        Raises:
            Exception: If any error occurs during the process.
        """
        backup_dir = './backup'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        try:
            for file in os.listdir('.'):
                if file.endswith('.json'):
                    with open(file, 'r') as f:
                        data = json.load(f)
                    trainer_id = data.get('trainerId')
                    if trainer_id is not None:
                        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                        base_filename = f'base_{trainer_id}.json'
                        base_filepath = os.path.join(backup_dir, base_filename)
                        
                        if os.path.exists(base_filepath):
                            backup_filename = f'backup_{trainer_id}_{timestamp}.json'
                            backup_filepath = os.path.join(backup_dir, backup_filename)
                            shutil.copy(file, backup_filepath)
                        else:
                            shutil.copy(file, base_filepath)
                        cFormatter.print(Color.GREEN, 'Backup created.', isLogging=True)    
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function create_backup(): {e}', isLogging=True)

    def restore_backup(self) -> None:
        """
        Restore a backup of JSON files.

        Example:
            restore_backup()
            # Output:
            # 1: base_123.json         <- Created on first edit
            # 2: backup_123_20230101_121212.json
            # Enter the number of the file you want to restore: 2
            # Data restored.

        Raises:
            Exception: If any error occurs during the process.
        """
        try:
            backup_dir = './backup'
            files = os.listdir(backup_dir)
            
            # Filtering and sorting files
            base_files = sorted(f for f in files if re.match(r'base_\d+\.json', f))
            backup_files = sorted(
                (f for f in files if re.match(r'backup_\d+_\d{8}_\d{6}\.json', f)),
                key=lambda x: (re.findall(r'\d+', x)[0], re.findall(r'\d{8}_\d{6}', x)[0])
            )
            
            all_files = base_files + backup_files
            
            if not all_files:
                cFormatter.print(Color.INFO, 'No backup files found.')
                return
            
            # Displaying sorted list with numbers
            for idx, file in enumerate(all_files, 1):
                sidenote = '        <- Created on first edit' if file.startswith('base_') else ''
                cFormatter.print(Color.GREEN, f'{idx}{Style.RESET_ALL}: {file} {sidenote}')

            cFormatter.print_separators(31, '-', Color.WHITE)

            # Getting user's choice
            while True:
                try:
                    choice = int(input('Enter the number of the file you want to restore: '))
                    if 1 <= choice <= len(all_files):
                        chosen_file = all_files[choice - 1]
                        chosen_filepath = os.path.join(backup_dir, chosen_file)
                        
                        # Determine the output filepath
                        parent_dir = os.path.abspath(os.path.join(backup_dir, os.pardir))
                        output_filepath = os.path.join(parent_dir, './trainer.json')
                        
                        # Copy the chosen file to the output filepath
                        shutil.copyfile(chosen_filepath, output_filepath)
                        cFormatter.print(Color.INFO, f'Data restored.')
                        break
                    else:
                        cFormatter.print(Color.WARNING, f'Invalid choice. Please enter a number within range.')
                except ValueError:
                    cFormatter.print(Color.WARNING, f'Invalid choice. Please enter a valid number.', isLogging=True)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function restore_backup(): {e}', isLogging=True)

    def another_update_all(self):
        url = "https://api.pokerogue.net/savedata/updateall"

        if "trainer.json" not in os.listdir():
            print("trainer.json file not found!")
            return
        with open("trainer.json", "r") as f:
            trainer_data = json.load(f)
        
        slot = self.slot
        if slot > 5 or slot < 1:
            print("Invalid slot number")
            return
        filename = f"slot_{slot}.json"
        if filename not in os.listdir():
            print(f"{filename} not found")
            return

        with open(filename, "r") as f:
            game_data = json.load(f)
        try:
            payload = {'clientSessionId': self.clientSessionId, 'session': game_data, "sessionSlotId": slot-1, 'system': trainer_data}
            response = self.session.post(url=url, headers=self.headers, json=payload)
            if response.status_code == 400:
                    print("Please do not play Pokerogue while using this tool. Restart the tool!")
                    return
            response.raise_for_status()
            print("Updated data Succesfully!")
            return
        except requests.exceptions.RequestException as e:
                cFormatter.print(Color.BRIGHT_RED, 'Response 403 - Forbidden. We have no authoriazion to acces the resource.', isLogging=True)
                cFormatter.print(Color.BRIGHT_RED, 'Please report to our GitHub.', isLogging=True)

    def unlock_all_starters(self) -> None:
        """
        Allows to unlock various options for starters and updates the local .json
        
        Raises:
            Exception: If any error occurs during the process.
        """
        try:
            trainer_data = self.__load_data('trainer.json')

            choice = int(input('Do you want to unlock all forms of the pokemon? (All forms are Tier 3 shinies. 1: Yes | 2: No): '))
            if (choice < 1) or (choice > 2):
                cFormatter.print(Color.INFO, f'Incorrect command. Setting to NO')
                choice = 2
            elif choice == 1:
                caught_attr = self.__MAX_BIG_INT
            else:
                choice = int(input('Make the Pokemon shiny? (1: Yes, 2: No): '))

                if (choice < 1) or (choice > 2):
                    cFormatter.print(Color.INFO, 'Invalid choice. Setting to NO')
                    choice = 2
                elif choice == 2:
                    caught_attr = 253
                else:
                    choice = int(input('What tier shiny do you want? (1: Tier 1, 2: Tier 2, 3: Tier 3, 4: All shinies): '))
                    if (choice < 1) or (choice > 4):
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
            if (iv < 1) or (iv > 2):
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                iv = 2
            
            passive: int = int(input('Do you want the starters to have the passive unlocked? (1: Yes | 2: No): '))
            if (passive < 1) or (passive > 2):
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                passive = 2
            
            ribbon: int = int(input('Do you want to unlock win-ribbons?: (1: Yes | 2: No): '))
            if (ribbon < 1) or (ribbon > 2):
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                ribbon = 2

            nature: int = int(input('Do you want to unlock all natures?: (1: Yes | 2: No): '))
            if (nature < 1) or (nature > 2):
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                nature = 2

            costReduce = int(input('How much do you want to reduce the cost? Yes lugia can cost nearly 0! (Number between 1 and 20): '))
            if (costReduce < 0) or (costReduce > 20):
                cFormatter.print(Color.INFO, 'Invalid input. Setting to 0.')
                costReduce = 0

            abilityAttr = int(input('Do you want to unlock all abilites? (1: Yes | 2: No): '))
            if (abilityAttr < 1) or (abilityAttr > 2):
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
        """
        try:
            trainer_data = self.__load_data('trainer.json')
            
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

            choice = int(input('Do you want to unlock all forms of the pokemon? (All forms are Tier 3 shinies. 1: Yes, 2: No): '))
            if (choice < 1) or (choice > 2):
                cFormatter.print(Color.INFO, f'No pokemon with ID: {dexId}')
                return
            elif choice == 1:
                caught_attr = self.__MAX_BIG_INT
            else:
                choice = int(input('Make the Pokemon shiny? (1: Yes, 2: No): '))

                if (choice < 1) or (choice > 2):
                    cFormatter.print(Color.INFO, 'Invalid choice. Setting to NO')
                    choice
                elif choice == 2:
                    caught_attr = 253
                else:
                    choice = int(input('What tier shiny do you want? (1: Tier 1, 2: Tier 2, 3: Tier 3, 4: All shinies): '))
                    if (choice < 1) or (choice > 4):
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
                
            caught = int(input('How many of this Pokemon have you caught?: '))
            hatched = int(input('How many of this Pokemon have hatched from eggs?: '))
            seen_count = int(input('How many of this Pokemon have you seen?: '))
            candies = int(input('How many candies do you want?: '))
            cFormatter.print(Color.INFO, 'Choose a value between 1 and 31 for your IVs (Pokemon Stats).')
            ivs = [int(input('SpA IVs: ')), int(input('DEF IVs: ')), int(input('Attack IVs: ')),
                int(input('HP IVs: ')), int(input('Spe IVs: ')), int(input('Def IVs: '))]
            
            passive: int = int(input('Do you want the starters to have the passive unlocked? (1: Yes | 2: No): '))
            if (passive < 1) or (passive > 2):
                cFormatter.print(Color.INFO, 'Invalid input. Setting to NO.')
                passive = 2
            elif passive == 1:
                if dexId in self.passive_data['noPassive']:
                    cFormatter.print(Color.INFO, 'This pokemon has no passive.')
                    passiveAttr = 0
                else:
                    passiveAttr = 3
            else:
                passiveAttr = 0
            
            costReduce = int(input('How much do you want to reduce the cost? Yes lugia can cost nearly 0! (Number between 1 and 20): '))
            if (costReduce < 0) or (costReduce > 20):
                cFormatter.print(Color.INFO, 'Invalid input. Setting to 0.')
                costReduce = 0

            abilityAttr = int(input('Do you want to unlock all abilites? (1: Yes, with hidden | 2: No): '))
            if (abilityAttr < 1) or (abilityAttr > 2):
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
            None
        """
        try:
            trainer_data = self.__load_data('trainer.json')

            c: int = int(input('How many common vouchers do you want: '))

            r: int = int(input('How many rare vouchers do you want: '))

            e: int = int(input('How many epic vouchers do you want: '))

            l: int = int(input('How many legendary vouchers do you want: '))

            voucher_counts: dict[str, int] = {
                '0': c,
                '1': r,
                '2': e,
                '3': l
            }
            trainer_data['voucherCounts'] = voucher_counts

            self.__write_data(trainer_data, 'trainer.json')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function add_tickets(): {e}', isLogging=True)

    def edit_pokemon_party(self) -> None:
            """
            Allows the user to edit the Pokemon party.
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
                cFormatter.print(Color.WHITE, f'\n'.join(options))
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

        This method unlocks all game modes for the player in the game data.

        Returns:
            None
        """
        trainer_data = self.__load_data('trainer.json')

        try:
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

        This method unlocks all achievements for the player in the game data.

        Returns:
            None
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
        Unlocks all vouchers for the player.

        This method generates random unlock times for each voucher and updates the game data accordingly.

        Returns:
            None
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
        Prints the contents of the NaturesEnum.
        """
        pokemons = [f'{member.value}: {member.name}' for member in self.pokemon_id_by_name]
        cFormatter.print(Color.WHITE, '\n'.join(pokemons))

    def print_biomes(self) -> None:
        """
        Prints all biomes available in the game.

        This method prints out all the biomes available in the game.

        Returns:
            None
        """
        biomes = [f'{member.value}: {member.name}' for member in self.biomes_by_id]
        cFormatter.print(Color.WHITE, '\n'.join(biomes))

    def print_moves(self) -> None:
        """
        Prints all moves available in the game.

        This method prints out all the moves available in the game.

        Returns:
            None, just does print.
        """
        moves = [f'{member.value}: {member.name}' for member in self.moves_by_id]
        cFormatter.print(Color.WHITE, '\n'.join(moves))

    def print_natures(self) -> None:
        """
        Prints all moves available in the game.

        This method prints out all the natures available in the game.

        Returns:
            None, just does print.
        """
        natures = [f'{member.value}: {member.name}' for member in self.nature_data]
        cFormatter.print(Color.WHITE, '\n'.join(natures))
    
    def print_vouchers(self) -> None:
        """
        Prints all moves available in the game.

        This method prints out all the vouchers available in the game.

        Returns:
            None, just does print.
        """
        vouchers = [f'{member.value}: {member.name}' for member in self.vouchers_data]
        cFormatter.print(Color.WHITE, '\n'.join(vouchers))

    def print_natureSlot(self) -> None:
        """
        Prints all moves available in the game.

        This method prints out all the natureSlot IDs available in the game.
        ## Do we need to sanitize with trys?
        Returns:
            None, just does print.
        """
        natureSlot = [f'{member.value}: {member.name}' for member in self.natureSlot_data]
        cFormatter.print(Color.WHITE, '\n'.join(natureSlot))
    
    def add_candies(self, dexId=None) -> None:
        """
        Adds candies to a Pokémon.

        This method allows the player to add candies to a specific Pokémon.

        Args:
            dexId (str): The ID of the Pokémon. Defaults to None.

        Returns:
            None
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

        This method allows the player to edit the biome of the game.

        Returns:
            None
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
            cFormatter.print(Color.CRITICAL, f'Error in function edit_hatchwaves(): {e}', isLogging=True)

    def edit_pokeballs(self) -> None:
        """
        Edits the number of pokeballs in the game.

        This method allows the player to edit the number of different types of pokeballs in the game.

        Returns:
            None
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
        Edits the amount of poke dollars in the game.

        This method allows the player to edit the amount of poke dollars they have in the game.

        Returns:
            None
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

        This method allows the player to generate eggs with specified attributes and adds them to their inventory.

        Returns:
            None
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
                    f'You have max number of eggs, replace eggs? (0: Cancel, 1: Replace): '
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

            new_eggs = generate_eggs(tier, gacha_type, hatch_waves, count)

            if replace_or_add == '1':
                trainer_data['eggs'] = new_eggs
            elif replace_or_add == '2':
                trainer_data['eggs'].extend(new_eggs)
            
            cFormatter.print(Color.GREEN, f'[{count}] eggs got generated succesfully.')
            self.__write_data(trainer_data, 'trainer.json')
            

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function generate_eggs(): {e}', isLogging=True)

    def edit_account_stats(self) -> None:
        """
        Edits the statistics of the player's account.

        This method allows the player to edit various statistics related to their gameplay.

        Returns:
            None
        """
        try:
            trainer_data = self.__load_data('trainer.json')
            
            battles: int = int(input('How many battles: '))
            classicSessionsPlayed: int = int(input('How many classicSessionsPlayed: '))
            dailyRunSessionPlayed: int = int(input('How many dailyRunSessionPlayed: '))
            dailyRunSessionWon: int = int(input('How many dailyRunSessionWon: '))
            eggsPulled: int = int(input('How many ceggsPulled: '))
            endlessSessionsPlayed: int = int(input('How many endlessSessionsPlayed: '))
            epicEggsPulled: int = int(input('How many cepicEggsPulled: '))
            highestDamage: int = int(input('How many highestDamage: '))
            highestEndlessWave: int = int(input('How many highestEndlessWave: '))
            highestHeal: int = int(input('How many highestHeal: '))
            highestLevel: int = int(input('How many highestLevel: '))
            highestMoney: int = int(input('How many highestMoney: '))
            legendaryEggsPulled: int = int(input('How many legendaryEggsPulled: '))
            legendaryPokemonCaught: int = int(input('How many legendaryPokemonCaught: '))
            legendaryPokemonHatched: int = int(input('How many legendaryPokemonHatched: '))
            legendaryPokemonSeen: int = int(input('How many clegendaryPokemonSeen: '))
            manaphyEggsPulled: int = int(input('How many manaphyEggsPulled: '))
            mythicalPokemonCaught: int = int(input('How many mythicalPokemonCaught: '))
            mythicalPokemonHatched: int = int(input('How mythicalPokemonHatched: '))
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
                'playTime': playTime*60,
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

            self.__write_data(trainer_data, 'trainer.json')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_hatchwaves(): {e}', isLogging=True)

    def unlock_all_features(self) -> None:
        """
        Maximizes the statistics and attributes of the player's account.

        This method unlocks all game modes, achievements, vouchers, and starters. It also sets the account statistics
        to a specified value for various attributes.

        Returns:
            None
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
            Exception: If any error occurs during the process.
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

            else:
                cFormatter.print(Color.GREEN, 'You have no eggs to hatch.')
            
            self.__write_data(trainer_data, 'trainer.json')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in function edit_hatchwaves(): {e}', isLogging=True)
    
    def print_help(self) -> None:
        """
        Print helpful information for the user.

        This method prints various helpful messages for the user, including information
        about manual JSON editing, assistance through the program's GitHub page, release
        version details, and cautions about account safety and program authenticity.
        """
        cFormatter.print(Color.INFO, 'You can always edit your json manually aswell.')
        cFormatter.print(Color.INFO, 'If you need assistance please refer to the programs GitHub page.')
        cFormatter.print(Color.INFO, 'https://github.com/RogueEdit/onlineRogueEditor/.')
        cFormatter.print(Color.INFO, f'This is release version {modules.config.version} - please include that in your issue or question report.')
        cFormatter.print(Color.INFO, 'This version now also features a log file.')
        cFormatter.print(Color.INFO, 'We do not take responsibility if your accounts get flagged or banned, and')
        cFormatter.print(Color.INFO, 'you never know if there is a clone from this programm. If you are not sure please')
        cFormatter.print(Color.INFO, 'calculate the checksum of this binary and visit https://github.com/RogueEdit/onlineRogueEditor/')
        cFormatter.print(Color.INFO, 'to see the value it should have to know its original from source.')

    def print_changes(self) -> None:
        """
        Print helpful information for the user.

        This method prints various helpful messages for the user, including information
        about manual JSON editing, assistance through the program's GitHub page, release
        version details, and cautions about account safety and program authenticity.
        """
        cFormatter.print(Color.INFO, '- Rate limiting')
        cFormatter.print(Color.INFO, '- Added delay and such to appear more natural to the server')
        cFormatter.print(Color.INFO, '- New header generation')
        cFormatter.print(Color.INFO, '- When headers fail more often we renew them from remote source (Hotfixes)')
        cFormatter.print(Color.INFO, '- Added second login logic as fallback')
        cFormatter.print(Color.INFO, '- Refined some logic and fixed some bugs')
        cFormatter.print(Color.INFO, f'https://github.com/RogueEdit/onlineRogueEditor/ {modules.config.version}')
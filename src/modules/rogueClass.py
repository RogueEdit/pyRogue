import requests
import json
import random
import os
import traceback
import shutil
from typing import Dict, Any, Union, Optional, List

from modules.eggLogic import *



class Rogue:
    def __init__(self, auth_token: str, clientSessionId: str) -> None:
        self._MAX_BIG_INT = (2 ** 53) - 1
        self.auth_token = auth_token
        self.clientSessionId = clientSessionId
        self.slot = None
        self.headers = None
        self.user_agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
            # Add more user agents if needed
        ]
        self._setup_headers()

    def make_request(self, url: str, headers: dict = None) -> dict:
        """
        Make an HTTP GET request to the specified URL with optional headers.

        Args:
            url (str): The URL to make the request to.
            headers (dict, optional): Headers to include in the request. Defaults to None.

        Returns:
            dict: JSON response from the server.
        """

        try:
            with requests.session() as s:
                response = s.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                data = response.json()
                return data
        except requests.RequestException as e:
            print("failed to make request")
            return {}

    def _setup_headers(self):
        self.headers = {
            "Authorization": self.auth_token,
            "User-Agent": random.choice(self.user_agents),
            "Accept": "application/json",
            "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://pokerogue.net/",
            "Content-Type": "application/json",
            "content-encoding": "br",
            "Origin": "https://pokerogue.net/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty"
        }

        # Load other data if needed from JSON files

        with open("./data/pokemon.json") as f:
            self.pokemon_id_by_name = json.loads(f.read())

        with open("./data/biomes.json") as f:
            self.biomes_by_id = json.loads(f.read())

        with open("./data/moves.json") as f:
            self.moves_by_id = json.loads(f.read())

        with open("./data/data.json") as f:
            self.extra_data = json.loads(f.read())

        with open("./data/passive.json") as f:
            self.passive_data = json.loads(f.read())

    def get_trainer_data(self) -> dict | None:
        """
        Retrieve trainer data from the API.

        Returns:
            dict | None: Trainer data or None if an error occurred.
        """
        url = f"https://api.pokerogue.net/savedata/system"
        return self.make_request(url)


    def get_gamesave_data(self, slot: int = 1) -> dict | None:
        """
        Retrieve game save data for the specified slot.

        Args:
            slot (int): The slot number (1-5). Defaults to 1.

        Returns:
            dict | None: Game save data or None if an error occurred.
        """



        url = f"https://api.pokerogue.net/savedata/session?slot={slot - 1}"
        return self.make_request(url)

    def update_all(self) -> None:
        """
        Update all data to the server.
        """
        url = "https://api.pokerogue.net/savedata/updateall"

        if "trainer.json" not in os.listdir():
            print("trainer.json file not found!")
            return

        with open("trainer.json", "r") as f:
            trainer_data = json.load(f)

        if self.slot is None or self.slot > 5 or self.slot < 1:
            print("Invalid slot number!")
            return

        filename = f"slot_{self.slot}.json"
        if filename not in os.listdir():
            print(f"{filename} not found")
            return

        with open(filename, "r") as f:
            game_data = json.load(f)

        try:
            with requests.session() as s:
                payload = {
                    'clientSessionId': self.clientSessionId,
                    'session': game_data,
                    "sessionSlotId": self.slot - 1,
                    'system': trainer_data
                }
                response = s.post(url=url, headers=self.headers, json=payload)
                if response.status_code == 400:
                    print("Please do not play Pokerogue while using this tool. Restart the tool!")
                    return
                response.raise_for_status()
                print("Updated data successfully!")
        except requests.exceptions.RequestException as e:
            print(f"Exception during update_all() -> {e}. If the error persists, report on Github.")
            print("This usually does not mean something good.")

    def __create_backup(self) -> None:
        """
        Create a backup of trainer.json and slot data.
        """
        files = ["trainer.json", f"slot_{self.slot}.json"]
        backup_folder = "./backup/"

        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
            print("Backup folder created successfully.")

        for file_name in files:
            source_file = file_name
            destination_file = os.path.join(backup_folder, file_name)
            shutil.copy2(source_file, destination_file)
            print(f"File '{file_name}' backed up to '{backup_folder}'.")

    def restore_backup(self) -> None:
        """
        Restore data from backup files.
        """
        choice = int(input(f"What file do you want to recover? (1: trainer.json | 2: slot_{self.slot}.json): "))

        if choice not in (1, 2):
            print("Invalid choice.")
            return

        if choice == 1:
            trainer_data = self.__load_data("./backup/trainer.json")
            self.__write_data(trainer_data, "trainer.json")
            print("Data restored")
        elif choice == 2:
            game_data = self.__load_data(f"./backup/slot_{self.slot}.json")
            self.__write_data(game_data, f"slot_{self.slot}.json")
            print("Data restored")

    def dump_data(self, slot: int = 1) -> None:
        """
        Dump data from the API to local files.

        Args:
            slot (int): The slot number (1-5). Defaults to 1.

        """
        if not self.slot:
            slot = int(input("Enter slot (1-5): "))
            self.slot = slot
            if slot > 5 or slot < 1:
                print("Invalid slot number")
                return

        trainer_data = self.get_trainer_data()
        game_data = self.get_gamesave_data(slot)

        self.__write_data(trainer_data, "trainer.json")
        self.__write_data(game_data, f"slot_{slot}.json")

        self.__create_backup()

        print("Data dumped successfully!")

    def __load_data(self, file_path: str) -> dict:
        """
        Load data from a specified file path.

        Args:
            file_path (str): Path to the file to be loaded.

        Returns:
            dict: Loaded data.
        """
        with open(file_path, "r") as f:
            return json.load(f)
    

    def __write_data(self, data: Dict[str, Any], file: str) -> None:
        """
        Writes data to a JSON file.

        Args:
            data (Dict[str, Any]): The data to be written.
            file (str): The file path.

        Returns:
            None
        """
        with open(file, "w") as f:
            json.dump(data, f, indent=2)
        print("---> Command applied successfully, remember to update the data to the server when you're done! <--- ")

    def pokedex(self) -> None:
        """
        Prints the Pokémon dex.
        """
        dex = [f"{value}: {key}" for key, value in self.pokemon_id_by_name['dex'].items()]
        print("\n".join(dex))

    def unlock_all_starters(self) -> None:
        """
        Unlocks all starters.

        Returns:
            None
        """
        trainer_data = self.__load_data("trainer.json")
        if not trainer_data:
            print("There was something wrong with the data, please restart the tool.")
            return None

        choice: int = int(input("Do you want to unlock all forms (Shiny Tier 3) as well? (1: Yes | 2: No): "))
        if (choice < 1) or (choice > 2):
            print("Invalid command.")
            return
        elif choice == 2:
            is_shiny: int = int(input("Do you want the starters to be shiny? (1: Yes | 2: No): "))
            if (is_shiny < 1) or (is_shiny > 2):
                print("Invalid command.")
                return
            elif is_shiny == 1:
                shiny: int = 255
            else:
                shiny: int = 253
        
        iv: int = int(input("Do you want the starters to be 6 IVs? (1: Yes | 2: No): "))
        if (iv < 1) or (iv > 2):
            print("Invalid command.")
            return
        
        passive: int = int(input("Do you want the starters to have the passive unlocked? (1: Yes | 2: No): "))
        if (passive < 1) or (passive > 2):
            print("Invalid command.")
            return
        
        ribbon: int = int(input("Do you want to unlock win-ribbons?: (1: Yes | 2: No): "))

        total_caught: int = 0
        total_seen: int = 0
        for entry in trainer_data["dexData"].keys():
            caught: int = random.randint(150, 250)
            seen: int = random.randint(150, 350)
            total_caught += caught
            total_seen += seen
            randIv: List[int] = random.sample(range(20, 30), 6)

            trainer_data["dexData"][entry] = {
                "seenAttr": 479,
                "caughtAttr": self.__MAX_BIG_INT if choice == 1 else shiny,
                "natureAttr": 67108862,
                "seenCount": seen,
                "caughtCount": caught,
                "hatchedCount": 0,
                "ivs": randIv if iv == 2 else [31, 31, 31, 31, 31, 31]
            }
            trainer_data["starterData"][entry] = {
                "moveset": None,
                "eggMoves": 15,
                "candyCount": caught + 20,
                "friendship": random.randint(1, 300),
                "abilityAttr": 7,
                "passiveAttr": 0 if (entry in self.passive_data["noPassive"]) or (passive == 2) else 3,
                "valueReduction": 2,
                "classicWinCount": None if ribbon == 2 else random.randint(1, 5),
            }

            
            trainer_data["gameStats"]["battles"] = total_caught + random.randint(1, total_caught)
            trainer_data["gameStats"]["pokemonCaught"] = total_caught
            trainer_data["gameStats"]["pokemonSeen"] = total_seen
            trainer_data["gameStats"]["shinyPokemonCaught"] = len(trainer_data["dexData"]) * 2

            if ribbon == 1:
                trainer_data["gameStats"]["classicWinCount"] = random.randint(1, 50)

        self.__write_data(trainer_data, "trainer.json")

    def starter_edit(self, dexId: Optional[Union[str, int]] = None) -> None:
        """
        Edits a starter Pokémon.

        Args:
            dexId (Optional[Union[str, int]]): The ID or name of the Pokémon. Defaults to None.

        Returns:
            None
        """
        trainer_data = self.__load_data("trainer.json")       

        if not trainer_data:
            print("There was something wrong with the data, please restart the tool.")
            return None
        if not dexId:
            dexId = input("Enter Pokemon (Name / ID): ")
            if dexId.isnumeric():
                if dexId not in trainer_data["starterData"]:
                    print(f"No Pokemon with ID: {dexId}")
                    return
            else:
                dexId = self.pokemon_id_by_name["dex"].get(dexId.lower())
                if not dexId:
                    print(f"No Pokemon with ID: {dexId}")
                    return
                

        choice: int = int(input("Do you want to unlock all forms of the pokemon? (All forms are Tier 3 shinies. (1: Yes | 2: No)): "))

        if (choice < 1) or (choice > 2):
            print("Invalid command.")
            return
        elif choice == 1:
            caught_attr: int = self.__MAX_BIG_INT
        else:
            choice: int = int(input("Make the Pokemon shiny? (1: Yes | 2: No)): "))
            if (choice < 1) or (choice > 2):
                print("Invalid choice.")
                return
            elif choice == 2:
                caught_attr: int = 253
            else:
                choice: int = int(input("What tier shiny do you want? (1: Tier 1 | 2: Tier 2 | 3: Tier 3): "))
                if (choice < 1) or (choice > 4):
                    print("Invalid choice.")
                    return
                elif choice == 1:
                    caught_attr: int = 159
                elif choice == 2:
                    caught_attr: int = 191
                elif choice == 3:
                    caught_attr: int = 255

            
        nature_attr: int = 67108862
        caught_input = input("How many of this Pokemon have you caught?: ")
        caught_input: str = input("How many of this Pokemon have you caught? If empty, random: ")
        caught: int = random.randint(1, 100) if not caught_input else int(caught_input)

        hatched_input: str = input("How many of this Pokemon have hatched from eggs? If empty, random: ")
        hatched: int = random.randint(1, 100) if not hatched_input else int(hatched_input)

        seen_count_input: str = input("How many of this Pokemon have you seen? If empty, random: ")
        seen_count: int = random.randint(1, 100) if not seen_count_input else int(seen_count_input)

        candies_input: str = input("How many Candies do you want? If empty, random: ")
        candies: int = random.randint(1, 100) if not candies_input else int(candies_input)

        ivs: List[int] = [int(input("SpA IVs: ")), int(input("DEF IVs: ")), int(input("Attack IVs: ")),
               int(input("HP IVs: ")), int(input("Spe IVs: ")), int(input("Def IVs: "))]
        passive: int = int(input("Do you want to unlock the passive? (1: Yes | 2: No): "))
        ribbon: int = int(input("Do you want to unlock the win-ribbon?: (1: Yes | 2: No): "))

        friendship_input: str = input("How many of this Pokemon have you seen? If empty, random: ")
        friendship: int = random.randint(1, 300) if not friendship_input else int(friendship_input)

        if (passive < 1) or (passive > 2):
            print("Invalid command.")
            return
        elif passive == 1:
            if dexId in self.passive_data["noPassive"]:
                print("This pokemon doesn't have a passive ability.")
                passiveAttr: int = 0
            else:
                passiveAttr: int = 3
        else:
            passiveAttr: int = 0


        trainer_data["dexData"][dexId] = {
            "seenAttr": 479,
            "caughtAttr": caught_attr,
            "natureAttr": nature_attr,
            "seenCount": seen_count,
            "caughtCount": caught,
            "hatchedCount": hatched,
            "ivs": ivs
        }
        trainer_data["starterData"][dexId] = {
            "moveset": None,
            "eggMoves": 15,
            "candyCount": candies,
            "friendship": None if not friendship else friendship,
            "abilityAttr": 7,
            "passiveAttr": passiveAttr,
            "valueReduction": 2,
            "classicWinCount": None if ribbon == 2 else random.randint(1, 50)
        }

        if ribbon == 1:
                trainer_data["gameStats"]["classicWinCount"] = random.randint(1, 50)

        self.__write_data(trainer_data, "trainer.json")

    def egg_gacha(self) -> None:
        """
        Simulates an egg gacha.

        Allows the user to input the number of common, rare, epic, and legendary vouchers they want to use.
        Updates the voucher counts in the trainer data.

        Returns:
            None
        """
        trainer_data = self.__load_data("trainer.json")

        if not trainer_data:
            print("There was something wrong with the data, please restart the tool.")
            return None

        c: int = int(input("How many common vouchers do you want (Max 300)?: "))

        if c > 300:
            print("Cannot put more than 300 tickets, please retry.")
            return

        r: int = int(input("How many rare vouchers do you want (Max 150)?: "))

        if r > 150:
            print("Cannot put more than 150 tickets, please retry.")
            return

        e: int = int(input("How many epic vouchers do you want (Max 100)?: "))

        if e > 100:
            print("Cannot put more than 100 tickets, please retry.")
            return

        l: int = int(input("How many legendary vouchers do you want (Max 10)?: "))

        if l > 10:
            print("Cannot put more than 10 tickets, please retry.")
            return

        voucher_counts: dict[str, int] = {
            "0": c,
            "1": r,
            "2": e,
            "3": l
        }
        trainer_data["voucherCounts"] = voucher_counts

        self.__write_data(trainer_data, "trainer.json")


    def edit_pokemon_party(self) -> None:
        """
        Allows editing a Pokémon in the player's party.

        This method presents a menu of options to edit a Pokémon in the player's party
        including changing species, setting shininess, level, luck, IVs, and moves.

        Returns:
            None
        """
        slot = self.slot
        filename = f"slot_{slot}.json"

        game_data = self.__load_data(filename)
        
        if game_data is None:
            print("There was something wrong with the data, please restart the tool.")
            return
        
        if game_data["gameMode"] == 3:
            print("Cannot edit this property on Daily Runs.")
            return
        
        options = [
            "1: Change species",
            "2: Set it shiny",
            "3: Set Level",
            "4: Set Luck",
            "5: Set IVs",
            "6: Change a move on a pokemon in your team"
        ]
        
        party_num = int(input("Select the party slot of the Pokémon you want to edit (0-5): "))
        if party_num < 0 or party_num > 5:
            print("Invalid party slot.")
            return

        if party_num >= len(game_data["party"]):
            print("Selected party slot does not exist. Choose another.")
            return
        
        print("**************************** OPTIONS ****************************")
        print("\n".join(options))
        print("--------------------------------------------------------------------")
        
        command = int(input("Option: "))
        if command < 1 or command > 6:
            print("Invalid option")
            return
        
        if command == 1:
            poke_id = int(input("Choose the pokemon you'd like by ID: "))
            game_data["party"][party_num]["species"] = poke_id
        elif command == 2:
            game_data["party"][party_num]["shiny"] = True
            variant = int(input("Choose the shiny variant (from 0 to 2): "))
            if variant < 0 or variant > 2:
                print("Invalid shiny variant")
                return
            game_data["party"][party_num]["variant"] = variant
        elif command == 3:
            level = int(input("Choose the level: "))
            if level < 1:
                print("Invalid level")
                return
            game_data["party"][party_num]["level"] = level
        elif command == 4:
            luck = int(input("What luck level do you desire? (from 1 to 14): "))
            if luck < 1 or luck > 14:
                print("Invalid luck")
                return
            game_data["party"][party_num]["luck"] = luck
        elif command == 5:
            ivs = [int(input("SpA IVs: ")), int(input("DEF IVs: ")), int(input("Attack IVs: ")),
               int(input("HP IVs: ")), int(input("Spe IVs: ")), int(input("Def IVs: "))]
            game_data["party"][party_num]["ivs"] = ivs
        elif command == 6:
            move_slot = int(input("Select the move you want to change (from 0 to 3): "))
            if move_slot < 0 or move_slot > 3:
                print("Invalid move slot")
                return
            move = int(input("What move do you want (ID)? "))
            if move < 0 or move > 919:
                print("Invalid move")
                return
            game_data["party"][party_num]["moveset"][move_slot]["moveId"] = move

        self.__write_data(game_data, filename)
    
    def unlock_all_gamemodes(self) -> None:
        """
        Unlocks all game modes for the player.

        This method unlocks all game modes for the player in the game data.

        Returns:
            None
        """
        trainer_data = self.__load_data("trainer.json")

        if trainer_data is None:
            print("There was something wrong with the data, please restart the tool.")
            return

        try:
            unlocked_modes = trainer_data.get("unlocks", {})
            if not unlocked_modes:
                print("Unable to find data entry: unlocks")
                return

            for mode in unlocked_modes:
                unlocked_modes[mode] = True

            print("---> All gamemodes have been unlocked! Remember to update data!")

            self.__write_data(trainer_data, "trainer.json")
        
        except Exception as e:
            print(f"Error on unlock_all_gamemodes() -> {e}")

    def unlock_all_achievements(self) -> None:
        """
        Unlocks all achievements for the player.

        This method unlocks all achievements for the player in the game data.

        Returns:
            None
        """
        try:
            trainer_data = self.__load_data("trainer.json")

            if trainer_data is None:
                print("There was something wrong with the data, please restart the tool.")
                return

            current_time_ms = int(time.time() * 1000) 
            min_time_ms = current_time_ms - 3600 * 1000  

            achievements = self.extra_data["achievements"]
            trainer_data["achvUnlocks"] = {
                achievement: random.randint(min_time_ms, current_time_ms)
                for achievement in achievements
            }
            print("---> All achievements have been unlocked! Remember to update data!")

            self.__write_data(trainer_data, "trainer.json")

        except Exception as e:
            print(f"Error on unlock_all_achievements -> {e}")

    
    def unlock_all_vouchers(self) -> None:
        """
        Unlocks all vouchers for the player.

        This method generates random unlock times for each voucher and updates the game data accordingly.

        Returns:
            None
        """
        try:
            trainer_data = self.__load_data("trainer.json")

            if trainer_data is None:
                print("There was something wrong with the data, please restart the tool.")
                return

            current_time_ms = int(time.time() * 1000) 
            min_time_ms = current_time_ms - 3600 * 1000  

            vouchers = self.extra_data.get("vouchers", [])
            voucher_unlocks = {}
            for voucher in vouchers:
                random_time = min_time_ms + random.randint(0, current_time_ms - min_time_ms)
                voucher_unlocks[voucher] = random_time
            trainer_data["voucherUnlocks"] = voucher_unlocks

            print("---> All vouchers have been unlocked! Remember to update data!")

            self.__write_data(trainer_data, "trainer.json")

        except Exception as e:
            print(f"Error on unlock_all_vouchers -> {e}")

    def biomes(self) -> None:
        """
        Prints all biomes available in the game.

        This method prints out all the biomes available in the game.

        Returns:
            None
        """
        biomes = [f"{value}: {key}" for key, value in self.biomes_by_id['biomes'].items()]
        print("\n".join(biomes))

    def moves(self) -> None:
        """
        Prints all moves available in the game.

        This method prints out all the moves available in the game.

        Returns:
            None
        """
        moves = [f"{value}: {key}" for key, value in self.moves_by_id['moves'].items()]
        print("\n".join(moves))
    
    def add_candies(self, dexId=None) -> None:
        """
        Adds candies to a Pokémon.

        This method allows the player to add candies to a specific Pokémon.

        Args:
            dexId (str): The ID of the Pokémon. Defaults to None.

        Returns:
            None
        """
        trainer_data = self.__load_data("trainer.json")

        if not trainer_data:
            print("There was something wrong with the data, please restart the tool.")
            return None
        if not dexId:
            dexId = input("Enter Pokemon (Name / ID): ")
            if dexId.isnumeric():
                if dexId not in trainer_data["starterData"]:
                    print(f"No Pokemon with ID: {dexId}")
                    return
            else:
                dexId = self.pokemon_id_by_name["dex"].get(dexId.lower())
                if not dexId:
                    print(f"No Pokemon with ID: {dexId}")
                    return
                
        candies = int(input("How many : "))
        trainer_data["starterData"][dexId]["candyCount"] = candies

        self.__write_data(trainer_data, "trainer.json")
    

    def edit_biome(self) -> None:
        """
        Edits the biome of the game.

        This method allows the player to edit the biome of the game.

        Returns:
            None
        """

        game_data = self.__load_data(f"slot_{self.slot}.json")

        self.biomes()

        biome = int(input("Insert the biome ID: "))

        game_data["arena"]["biome"] = biome

        self.__write_data(game_data, f"slot_{self.slot}.json")
    
    def edit_pokeballs(self) -> None:
        """
        Edits the number of pokeballs in the game.

        This method allows the player to edit the number of different types of pokeballs in the game.

        Returns:
            None
        """
        game_data = self.__load_data(f"slot_{self.slot}.json")

        if game_data is None:
            print("There was something wrong with the data, please restart the tool.")
            return

        if game_data["gameMode"] == 3:
            print("Cannot edit this property on Daily Runs.")
            return

        choice = int(input("How many pokeballs do you want?: "))
        game_data["pokeballCounts"]["0"] = choice

        choice = int(input("How many great balls do you want?: "))
        game_data["pokeballCounts"]["1"] = choice

        choice = int(input("How many ultra balls do you want?: "))
        game_data["pokeballCounts"]["2"] = choice

        choice = int(input("How many rogue balls do you want?: "))
        game_data["pokeballCounts"]["3"] = choice

        choice = int(input("How many master balls do you want?: "))
        game_data["pokeballCounts"]["4"] = choice

        self.__write_data(game_data, f"slot_{self.slot}.json")

    
    def edit_money(self) -> None:
        """
        Edits the amount of poke dollars in the game.

        This method allows the player to edit the amount of poke dollars they have in the game.

        Returns:
            None
        """
        game_data = self.__load_data(f"slot_{self.slot}.json")

        if game_data is None:
            print("There was something wrong with the data, please restart the tool.")
            return

        if game_data["gameMode"] == 3:
            print("Cannot edit this property on Daily Runs.")
            return

        choice = int(input("How many poke dollars do you want?: "))
        game_data["money"] = choice

        self.__write_data(game_data, f"slot_{self.slot}.json")
    
    def generate_eggs(self) -> None:
        """
        Generates eggs for the player.

        This method allows the player to generate eggs with specified attributes and adds them to their inventory.

        Returns:
            None
        """
        try:
            trainer_data = self.__load_data("trainer.json")

            if trainer_data["eggs"] is not None:
                egg_len = len(trainer_data["eggs"])
            else:
                trainer_data["eggs"] = []
                egg_len = len(trainer_data["eggs"])
            
            if egg_len >= 75:
                replace_or_add = input(
                    f"You have max number of eggs, replace eggs? (0: Cancel, 1: Replace): "
                )
                if replace_or_add == "2":
                    replace_or_add = "1"
            else:
                replace_or_add = input(
                    f"You have [{egg_len}] eggs, add or replace eggs? (0: Cancel, 1: Replace, 2: Add): "
                )
                
            if replace_or_add not in ["1", "2"]:
                raise ValueError("Invalid replace_or_add selected!")
                
            max_count = 75 - egg_len if replace_or_add == "2" else 75
            
            count = int(
                input(f"How many eggs do you want to have? (0 - {max_count})(number): ")
            )
            tier = input(
                "What tier should the eggs have? (1: Common, 2: Rare, 3: Epic, 4: Legendary, 5: Manaphy): "
            )
            # Map tier to string
            tier_map = {
                "1": "COMMON",
                "2": "RARE",
                "3": "EPIC",
                "4": "LEGENDARY",
                "5": "MANAPHY"
            }
            if tier not in tier_map:
                raise ValueError("Invalid tier selected!")
            tier = tier_map[tier]
            
            gacha_type = input(
                "What gacha type do you want to have? (1: Move, 2: Legendary, 3: Shiny): "
            )
            # Map gacha type to string
            gacha_map = {
                "1": "MOVE",
                "2": "LEGENDARY",
                "3": "SHINY"
            }
            if gacha_type not in gacha_map:
                raise ValueError("Invalid gacha_type selected!")
            gacha_type = gacha_map[gacha_type]
            
            hatch_waves = int(
                input("After how many waves should they hatch? (0-100)(number): ")
            )

            new_eggs = generate_eggs(tier, gacha_type, hatch_waves, count)

            if replace_or_add == "1":
                trainer_data["eggs"] = new_eggs
            elif replace_or_add == "2":
                trainer_data["eggs"].extend(new_eggs)
                    
            self.__write_data(trainer_data, "trainer.json")
            
            print(f"[{count}] eggs got generated and uploaded!")

        except Exception as e:
            print(f"Something went wrong while generating the data: {e}")

    def edit_account_stats(self) -> None:
        """
        Edits the statistics of the player's account.

        This method allows the player to edit various statistics related to their gameplay.

        Returns:
            None
        """
        try:
            trainer_data = self.__load_data("trainer.json")

            if trainer_data is None:
                print("There was something wrong with the data, please restart the tool.")
                return
            
            battles: int = int(input("How many battles: "))
            classicSessionsPlayed: int = int(input("How many classicSessionsPlayed: "))
            dailyRunSessionPlayed: int = int(input("How many dailyRunSessionPlayed: "))
            dailyRunSessionWon: int = int(input("How many dailyRunSessionWon: "))
            eggsPulled: int = int(input("How many ceggsPulled: "))
            endlessSessionsPlayed: int = int(input("How many endlessSessionsPlayed: "))
            epicEggsPulled: int = int(input("How many cepicEggsPulled: "))
            highestDamage: int = int(input("How many highestDamage: "))
            highestEndlessWave: int = int(input("How many highestEndlessWave: "))
            highestHeal: int = int(input("How many highestHeal: "))
            highestLevel: int = int(input("How many highestLevel: "))
            highestMoney: int = int(input("How many highestMoney: "))
            legendaryEggsPulled: int = int(input("How many legendaryEggsPulled: "))
            legendaryPokemonCaught: int = int(input("How many legendaryPokemonCaught: "))
            legendaryPokemonHatched: int = int(input("How many legendaryPokemonHatched: "))
            legendaryPokemonSeen: int = int(input("How many clegendaryPokemonSeen: "))
            manaphyEggsPulled: int = int(input("How many manaphyEggsPulled: "))
            mythicalPokemonCaught: int = int(input("How many mythicalPokemonCaught: "))
            mythicalPokemonHatched: int = int(input("How mythicalPokemonHatched: "))
            mythicalPokemonSeen: int = int(input("How many mythicalPokemonSeen: "))
            playTime: int = int(input("How much playtime in hours: ")*60)
            pokemonCaught: int = int(input("How many pokemonCaught: "))
            pokemonDefeated: int = int(input("How many pokemonDefeated: "))
            pokemonFused: int = int(input("How many pokemonFused: "))
            pokemonHatched: int = int(input("How many pokemonHatched: "))
            pokemonSeen: int = int(input("How many pokemonSeen: "))
            rareEggsPulled: int = int(input("How many rareEggsPulled: "))
            ribbonsOwned: int = int(input("How many ribbonsOwned: "))
            sessionsWon: int = int(input("How many sessionsWon: "))
            shinyPokemonCaught: int = int(input("How many shinyPokemonCaught: "))
            shinyPokemonHatched: int = int(input("How many shinyPokemonHatched: "))
            shinyPokemonSeen: int = int(input("How many shinyPokemonSeen: "))
            subLegendaryPokemonCaught: int = int(input("How many subLegendaryPokemonCaught: "))
            subLegendaryPokemonHatched: int = int(input("How many subLegendaryPokemonHatched: "))
            subLegendaryPokemonSeen: int = int(input("How many subLegendaryPokemonSeen: "))
            trainersDefeated: int = int(input("How many trainersDefeated: "))

            trainer_data["gameStats"] = {
                "battles": battles,
                "classicSessionsPlayed": classicSessionsPlayed,
                "dailyRunSessionsPlayed": dailyRunSessionPlayed,
                "dailyRunSessionsWon": dailyRunSessionWon,
                "eggsPulled": eggsPulled,
                "endlessSessionsPlayed": endlessSessionsPlayed,
                "epicEggsPulled": epicEggsPulled,
                "highestDamage": highestDamage,
                "highestEndlessWave": highestEndlessWave,
                "highestHeal": highestHeal,
                "highestLevel": highestLevel,
                "highestMoney": highestMoney,
                "legendaryEggsPulled": legendaryEggsPulled,
                "legendaryPokemonCaught": legendaryPokemonCaught,
                "legendaryPokemonHatched": legendaryPokemonHatched,
                "legendaryPokemonSeen": legendaryPokemonSeen,
                "manaphyEggsPulled": manaphyEggsPulled,
                "mythicalPokemonCaught": mythicalPokemonCaught,
                "mythicalPokemonHatched": mythicalPokemonHatched,
                "mythicalPokemonSeen": mythicalPokemonSeen,
                "playTime": playTime,
                "pokemonCaught": pokemonCaught,
                "pokemonDefeated": pokemonDefeated,
                "pokemonFused": pokemonFused,
                "pokemonHatched": pokemonHatched,
                "pokemonSeen": pokemonSeen,
                "rareEggsPulled": rareEggsPulled,
                "ribbonsOwned": ribbonsOwned,
                "sessionsWon": sessionsWon,
                "shinyPokemonCaught": shinyPokemonCaught,
                "shinyPokemonHatched": shinyPokemonHatched,
                "shinyPokemonSeen": shinyPokemonSeen,
                "subLegendaryPokemonCaught": subLegendaryPokemonCaught,
                "subLegendaryPokemonHatched": subLegendaryPokemonHatched,
                "subLegendaryPokemonSeen": subLegendaryPokemonSeen,
                "trainersDefeated": trainersDefeated,
            }

            self.__write_data(trainer_data, "trainer.json")
        except Exception as e:
            print(f"Error on edit_account_stats() -> {e}")

    def max_account(self) -> None:
        """
        Maximizes the statistics and attributes of the player's account.

        This method unlocks all game modes, achievements, vouchers, and starters. It also sets the account statistics
        to a specified value for various attributes.

        Returns:
            None
        """
        try:
            trainer_data = self.__load_data("trainer.json")

            if trainer_data is None:
                print("There was something wrong with the data, please restart the tool.")
                return
            
            self.unlock_all_gamemodes()
            self.unlock_all_achievements()
            self.unlock_all_vouchers()
            self.unlock_all_starters()
        
            total_caught = 0
            total_seen = 0
            for entry in trainer_data["dexData"].keys():
                caught = random.randint(500, 1000)
                seen = random.randint(500, 1000)
                hatched = random.randint(500, 1000)
                total_caught += caught
                total_seen += seen
                randIv: List[int] = random.sample(range(20, 30), 6)

                trainer_data["dexData"][entry] = {
                    "seenAttr": self._MAX_BIG_INT,
                    "caughtAttr": self._MAX_BIG_INT,
                    "natureAttr": self._MAX_BIG_INT,
                    "seenCount": seen,
                    "caughtCount": caught,
                    "hatchedCount": hatched,
                    "ivs": randIv
                }

            trainer_data["gameStats"] = {
                "battles": total_caught + random.randint(1, total_caught),
                "classicSessionsPlayed": random.randint(2500, 10000) // 10,
                "dailyRunSessionsPlayed": random.randint(2500, 10000),
                "dailyRunSessionsWon": random.randint(2500, 10000),
                "eggsPulled": random.randint(2500, 10000),
                "endlessSessionsPlayed": random.randint(2500, 10000),
                "epicEggsPulled": random.randint(2500, 10000),
                "highestDamage": random.randint(2500, 10000),
                "highestEndlessWave": random.randint(2500, 10000),
                "highestHeal": random.randint(2500, 10000),
                "highestLevel": random.randint(2500, 10000),
                "highestMoney": random.randint(2500, 10000),
                "legendaryEggsPulled": random.randint(2500, 10000),
                "legendaryPokemonCaught": random.randint(2500, 10000),
                "legendaryPokemonHatched": random.randint(2500, 10000),
                "legendaryPokemonSeen": random.randint(2500, 10000),
                "manaphyEggsPulled": random.randint(2500, 10000),
                "mythicalPokemonCaught": random.randint(2500, 10000),
                "mythicalPokemonHatched": random.randint(2500, 10000),
                "mythicalPokemonSeen": random.randint(2500, 10000),
                "playTime": random.randint(2500, 10000) * 100,
                "pokemonCaught": total_caught,
                "pokemonDefeated": random.randint(2500, 10000),
                "pokemonFused": random.randint(2500, 10000),
                "pokemonHatched": random.randint(2500, 10000),
                "pokemonSeen": total_seen,
                "rareEggsPulled": random.randint(2500, 10000),
                "ribbonsOwned": total_seen,
                "sessionsWon": random.randint(2500, 10000),
                "shinyPokemonCaught": len(list(trainer_data["dexData"])) * 2,
                "shinyPokemonHatched": random.randint(2500, 10000),
                "shinyPokemonSeen": random.randint(2500, 10000),
                "subLegendaryPokemonCaught": random.randint(2500, 10000),
                "subLegendaryPokemonHatched": random.randint(2500, 10000),
                "subLegendaryPokemonSeen": random.randint(2500, 10000),
                "trainersDefeated": random.randint(2500, 10000),
            }

            self.__write_data(trainer_data, "trainer.json")
        except Exception as e:
            print(f"Error on edit_account_stats() -> {e}")


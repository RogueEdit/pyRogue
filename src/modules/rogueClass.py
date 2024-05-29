import requests, json, random, os, time
import brotli
import traceback
import shutil

from modules.eggLogic import *


class Rogue:
    def __init__(self, auth_token, clientSessionId):
        self.auth_token = auth_token
        self.clientSessionId = clientSessionId
        self.headers = {
            "authorization": self.auth_token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
            "Accept": "application/json",
            "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://pokerogue.net/",
            "Content-Type": "application/json",
            "content-encoding": "br",
            "Origin": "https://pokerogue.net/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=1",
        }

        self.slot = None

        self.__MAX_BIG_INT = (2 ** 53) - 1

        
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
        
        self.__dump_data()
        



    def __make_request(self, url):
        try:
            with requests.session() as s:
                response = s.get(url, headers=self.headers)
                response.raise_for_status()

                try:
                    json_response = response.json()
                    return json_response
                except json.JSONDecodeError as e:
                    print("Failed to parse response as JSON:", e)
                    traceback.print_exc()  
                    return None

        except requests.exceptions.RequestException as e:
            print(f"Exception during request -> {e}")
            return None

    def get_trainer_data(self):
        url = f"https://api.pokerogue.net/savedata/system?clientSessionId={self.clientSessionId}"
        return self.__make_request(url)

    def get_gamesave_data(self, slot=1):
        url = f"https://api.pokerogue.net/savedata/session?slot={slot-1}&clientSessionId={self.clientSessionId}"
        return self.__make_request(url)

    def update_all(self):
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
            with requests.session() as s:
                payload = {'clientSessionId': self.clientSessionId, 'session': game_data, "sessionSlotId": slot-1, 'system': trainer_data}
                response = s.post(url=url, headers=self.headers, json=payload)
                if response.status_code == 400:
                        print("Please do not play Pokerogue while using this tool. Restart the tool!")
                        return
                response.raise_for_status()
                print("Updated data Succesfully!")
                return
        except requests.exceptions.RequestException as e:
                print(f"Exception during update_all() -> {e}. If the error persists, report on Github.")

    
    def __create_backup(self):

        files = ["trainer.json", f"slot_{self.slot}.json"]

        backup_folder = "./backup/"

        if not os.path.exists(backup_folder):
            os.makedirs("./backup/")
            print("Backup folder created successfully.")

        for file_name in files:
            source_file = file_name
            destination_file = os.path.join(backup_folder, file_name)
            shutil.copy2(source_file, destination_file)
            print(f"File '{file_name}' backed up to '{backup_folder}'.")

    
    def restore_backup(self):

        choice = int(input(f"What file do you wanna recover?(1: trainer.json, 2: slot_{self.slot}.json): "))

        if (choice < 1) or (choice > 2):
            print("Invalid choice.")
            return
        elif choice == 1:
            trainer_data = self.__load_data("./backup/trainer.json")
            self.__write_data(trainer_data, "trainer.json")
            print("Data restored")
        elif choice == 2:
            game_data = self.__load_data(f"./backup/slot_{self.slot}.json")
            self.__write_data(game_data, f"slot_{self.slot}.json")
            print("Data restored")

        
    def __dump_data(self, slot=None):
        data = self.get_trainer_data()
        if not data:
            return None
        with open("trainer.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Trainer data dumped to 'trainer.json'")

        if not slot:
            slot = int(input("Enter slot (1-5): "))
            self.slot = slot
            if slot > 5 or slot < 1:
                print("Invalid slot number")
                return
        data = self.get_gamesave_data(slot)
        if not data:
            print("No gamesave file available in that slot, Kill at least 1 pokemon and progress to stage two")
            print("When finished, launch the tool again.")
            return None
        with open(f"slot_{slot}.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"Gamesave data for slot {slot} dumped to 'slot_{slot}.json'")

        self.__create_backup()

        
    
    def __load_data(self, file):
        if not os.path.exists(file):
            print(f"{file} file not found!")
            return
        with open(file, "r") as f:
            data = json.load(f)
            return data
    

    def __write_data(self, data, file):
        with open(file, "w") as f:
            json.dump(data, f, indent=2)
        print("Command applied successfully, remember to update the data to the server when you're done!")


    def pokedex(self):
        dex = [f"{value}: {key}" for key, value in self.pokemon_id_by_name['dex'].items()]
        print("\n".join(dex))

    def unlock_all_starters(self):

        trainer_data = self.__load_data("trainer.json")

        if not trainer_data:
            print("There was something wrong with the data, please restart the tool.")
            return None

        choice = int(input("Do you want to unlock all forms(shiny tier 3) as well?(1: yes, 2: no): "))

        if (choice < 1) or (choice > 2):
            print("Invalid command.")
            return
        elif choice == 2:
            is_shiny = int(input("Do you want the starters to be shiny?(1: yes, 2: no): "))

            if (is_shiny < 1) or (is_shiny > 2):
                print("Invalid command.")
                return
            elif is_shiny == 1:
                shiny = 255
            else:
                shiny = 253
        
        iv = int(input("Do you want the starters to be 6 IVs?(1: yes, 2: no): "))
        if (iv < 1) or (iv > 2):
            print("Invalid command.")
            return
        
        passive = int(input("Do you want the starters to have the passive unlocked?(1: yes, 2: no): "))
        if (passive < 1) or (passive > 2):
            print("Invalid command.")
            return

        total_caught = 0
        total_seen = 0
        for entry in trainer_data["dexData"].keys():
            caught = random.randint(150, 250)
            seen = random.randint(150, 350)
            total_caught += caught
            total_seen += seen
            randIv = random.sample(range(20, 30), 6)

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
                "abilityAttr": 7,
                "passiveAttr": 0 if (entry in self.passive_data["noPassive"]) or (passive == 2) else 3,
                "valueReduction": 2
            }
            trainer_data["gameStats"]["battles"] = total_caught + random.randint(1, total_caught)
            trainer_data["gameStats"]["pokemonCaught"] = total_caught
            trainer_data["gameStats"]["pokemonSeen"] = total_seen
            trainer_data["gameStats"]["shinyPokemonCaught"] = len(trainer_data["dexData"]) * 2

        self.__write_data(trainer_data, "trainer.json")

    def starter_edit(self, dexId=None):
        
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
                

        choice = int(input("Do you want to unlock all forms of the pokemon?(All forms are Tier 3 shinies. 1: Yes, 2: No): "))

        if (choice < 1) or (choice > 2):
            print("Invalid command.")
            return
        elif choice == 1:
            caught_attr = self.__MAX_BIG_INT
        else:
            choice = int(input("Make the Pokemon shiny? (1: Yes, 2: No): "))

            if (choice < 1) or (choice > 2):
                print("Invalid choice.")
                return
            elif choice == 2:
                caught_attr = 253
            else:
                choice = int(input("What tier shiny do you want? (1: Tier 1, 2: Tier 2, 3: Tier 3, 4: All shinies): "))
                if (choice < 1) or (choice > 4):
                    print("Invalid choice.")
                    return
                elif choice == 1:
                    caught_attr = 159
                elif choice == 2:
                    caught_attr = 191
                elif choice == 3:
                    caught_attr = 223
                else:
                    caught_attr = 255
            
        nature_attr = 67108862
        caught = int(input("How many of this Pokemon have you caught?: "))
        hatched = int(input("How many of this Pokemon have hatched from eggs?: "))
        seen_count = int(input("How many of this Pokemon have you seen?: "))
        candies = int(input("How many candies do you want?: "))
        ivs = [int(input("SpA IVs: ")), int(input("DEF IVs: ")), int(input("Attack IVs: ")),
               int(input("HP IVs: ")), int(input("Spe IVs: ")), int(input("Def IVs: "))]
        
        passive = int(input("Do you want to unlock the passive?(1: Yes, 2: No): "))
        if (passive < 1) or (passive > 2):
            print("Invalid command.")
            return
        elif passive == 1:
            if dexId in self.passive_data["noPassive"]:
                print("This pokemon doesn't have a passive ability.")
                passiveAttr = 0
            else:
                passiveAttr = 3
        else:
            passiveAttr = 0
        

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
            "abilityAttr": 7,
            "passiveAttr": passiveAttr,
            "valueReduction": 2
        }

        self.__write_data(trainer_data, "trainer.json")


    def egg_gacha(self):

        trainer_data = self.__load_data("trainer.json")

        if not trainer_data:
            print("There was something wrong with the data, please restart the tool.")
            return None

        c = int(input("How many common vouchers do you want(Max 300)?: "))

        if c > 300:
            print("Cannot put more than 300 tickets, please retry.")
            return

        r = int(input("How many rare vouchers do you want(Max 150)?: "))
        
        if r > 150:
            print("Cannot put more than 150 tickets, please retry.")
            return
        
        e = int(input("How many epic vouchers do you want(Max 100)?: "))

        if e > 100:
            print("Cannot put more than 100 tickets, please retry.")
            return
        
        l = int(input("How many legendary vouchers do you want(Max 10)?: "))

        if l > 10:
            print("Cannot put more than 10 tickets, please retry.")
            return


        voucher_counts = {
            "0": c,
            "1": r,
            "2": e,
            "3": l
        }
        trainer_data["voucherCounts"] = voucher_counts

        self.__write_data(trainer_data, "trainer.json")

    # def hatch_all_eggs(self):

    #     trainer_data = self.__load_data("trainer.json")

    #     if not trainer_data:
    #         return None
    #     eggs = trainer_data.get("eggs", [])
    #     if not eggs:
    #         print("No eggs to hatch")
    #         return
    #     for egg in eggs:
    #         egg["hatchWaves"] = 0
    #     trainer_data["eggs"] = eggs


    #     self.__write_data(trainer_data, "trainer.json")
        
    
    def edit_pokemon_party(self):
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
            print("Invalid party slot")
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
    
    def unlock_all_gamemodes(self):

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

            print("All gamemodes have been unlocked! Remember to update data!")

            self.__write_data(trainer_data, "trainer.json")
        
        except Exception as e:
            print(f"Error on unlock_all_gamemodes() -> {e}")
    
    def unlock_all_achievements(self):
        
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
            print("All achievements have been unlocked! Remember to update data!")

            self.__write_data(trainer_data, "trainer.json")

        except Exception as e:
            print(f"Error on unlock_all_achievements -> {e}")

    
    def unlock_all_vouchers(self):
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

            print("All vouchers have been unlocked! Remember to update data!")

            self.__write_data(trainer_data, "trainer.json")

        except Exception as e:
            print(f"Error on unlock_all_vouchers -> {e}")
    
    def biomes(self):
        biomes = [f"{value}: {key}" for key, value in self.biomes_by_id['biomes'].items()]
        print("\n".join(biomes))

    def moves(self):
        moves = [f"{value}: {key}" for key, value in self.moves_by_id['moves'].items()]
        print("\n".join(moves))
    
    def add_candies(self, dexId=None):
    
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
                
        candies = int(input("How many candies do you want?: "))
        trainer_data["starterData"][dexId]["candyCount"] = candies

        self.__write_data(trainer_data, "trainer.json")
    

    def edit_biome(self):
        game_data = self.__load_data(f"slot_{self.slot}.json")

        biome = int(input("Insert the biome ID: "))

        game_data["arena"]["biome"] = biome

        self.__write_data(game_data, f"slot_{self.slot}.json")
    
    def edit_pokeballs(self):
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

    
    def edit_money(self):
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
    
    def generate_eggs(self):

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

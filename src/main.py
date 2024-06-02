import logging
import getpass
import requests
from modules.loginLogic import loginLogic
from modules.rogueClass import Rogue
from colorama import Fore, Style, init

#Initialize colorama
init()

# Configure logging to display debug messages
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    session = requests.Session()
    
    while True:
        print(Fore.GREEN + "\n<PyRogue Login>" + Style.RESET_ALL)
        username = input("Username: ")
        password = getpass.getpass("Password (password is hidden): ")
        print("--------------------------")

        login = loginLogic(username, password)

        try:
            if login.login():
                print(f"Logged in as: {username.capitalize()}")
                rogue = Rogue(session, login.token, login.session_id)
                
                # Call the dump_data method after successful login
                rogue.dump_data()
                
                break
            else:
                print("Incorrect credentials")
        except Exception as e:
            print("An error occurred during login.")
            logging.exception(e)
            
    func = {
        "1": rogue.get_trainer_data,
        "2": rogue.get_gamesave_data,
        "3": rogue.starter_edit,
        "4": rogue.unlock_all_starters,
        "5": rogue.egg_gacha,
        "6": rogue.edit_pokemon_party,
        "7": rogue.unlock_all_achievements,
        "8": rogue.unlock_all_gamemodes,
        "9": rogue.unlock_all_vouchers,
        "10": rogue.add_candies,
        "11": rogue.edit_money,
        "12": rogue.edit_pokeballs,
        "13": rogue.edit_biome,
        "14": rogue.generate_eggs,
        "15": rogue.edit_account_stats,
        "16": rogue.max_account,
        "17": rogue.restore_backup,
        "18": rogue.pokedex,
        "19": rogue.biomes,
        "20": rogue.moves,
        "21": rogue.update_all
    }

    title = "************************ PyRogue *************************"
    working_status = "(Working)"

    formatted_title = f"{Fore.GREEN}{Style.BRIGHT}{title}{Style.RESET_ALL}"
    formatted_working_status = f"{Fore.GREEN}{Style.BRIGHT}{working_status}{Style.RESET_ALL}"

    term = [
        f"{formatted_title}",
        f"1: Load Game-Data from server{' ' * 20}{formatted_working_status}",
        f"2: Load SaveSlot-Data from server{' ' * 16}{formatted_working_status}",
        f"3: Edit a starter{' ' * 32}{formatted_working_status}",
        f"4: Unlock all starters{' ' * 27}{formatted_working_status}",
        f"5: Edit your egg-tickets{' ' * 25}{formatted_working_status}",
        f"6: Edit CURRENT Pokemon Party{' ' * 20}{formatted_working_status}",
        f"7: Unlock all achievements{' ' * 23}{formatted_working_status}",
        f"8: Unlock all gamemodes{' ' * 26}{formatted_working_status}",
        f"9: Unlock all vouchers{' ' * 27}{formatted_working_status}",
        f"10: Add candies to a pokemon{' ' * 21}{formatted_working_status}",
        f"11: Edit money amount{' ' * 28}{formatted_working_status}",
        f"12: Edit pokeballs amount{' ' * 24}{formatted_working_status}",
        f"13: Edit biome{' ' * 35}{formatted_working_status}",
        f"14: Generate eggs{' ' * 32}{formatted_working_status}",
        f"15: Edit account stats{' ' * 27}{formatted_working_status}",
        f"16: Unlock Everything{' ' * 28}{formatted_working_status}",
        "----------------------------------------------------------",
        f"17: Recover your backup{' ' * 26}{formatted_working_status}",
        f"18: Show all Pokemon ID{' ' * 26}{formatted_working_status}",
        f"19: Show all Biome IDs{' ' * 27}{formatted_working_status}",
        f"20: Show all Move IDs{' ' * 28}{formatted_working_status}",
        "----------------------------------------------------------",
        f"21: >> Save data and upload to the Server{' ' * 17}{formatted_working_status}",
        f"{formatted_title}",
    ]
    while True:
        print("")
        for line in term:
            print(Fore.GREEN + "* " + Style.RESET_ALL + line + Fore.GREEN + " *" + Style.RESET_ALL)
        command = input("Command: ")

        if command in func:
            func[command]()
        elif command == "exit":
            quit()
        else:
            print("Command not found")
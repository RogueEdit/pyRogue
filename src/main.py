# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 04.06.2024 

import logging
import getpass
import requests
import brotli
from modules.loginLogic import loginLogic
from modules.mainLogic import Rogue
from colorama import Fore, Style, init
<<<<<<< HEAD

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 5772c92 (removed brotli)
#Initialize colorama
=======
>>>>>>> 9225a9d (Logic Refactoring, Ultimate additions)
=======
from utilities.cFormatter import cFormatter, Color
# cFormatter.print(Color.INFO, 'This is a test message', isLogging=True)
# [CYAN]This is a test message[RESET]
# cFormatter.print_separators(10, '-', Color.GREEN)
# [GREEN]----------[RESET]

from utilities.logger import CustomLogger

>>>>>>> 68279c3 (More logic rewrite)
init()

logger = CustomLogger()

if __name__ == '__main__':
    session = requests.Session()
    
    while True:
        print('')
        cFormatter.print(Color.GREEN, '<pyRogue>')
        username = input('Username: ')
        password = getpass.getpass('Password (password is hidden): ')

        login = loginLogic(username, password)

        try:
            if login.login():
                cFormatter.print(Color.INFO, f'Logged in as: {username.capitalize()}')
                rogue = Rogue(session, login.token, login.session_id)
                
                break
            else:
                cFormatter.print(Color.INFO, 'Wrong credentials.', isLogging=True)
        except Exception as e:
            cFormatter.print(Color.GREEN, f'Something went wrong. {e}', isLogging=True)
            
    func = {
        '1': rogue.get_trainer_data,
        '2': rogue.get_gamesave_data,
        '3': rogue.edit_starter_separate,
        '4': rogue.unlock_all_starters,
        '5': rogue.add_ticket,
        '6': rogue.edit_pokemon_party,
        '7': rogue.unlock_all_achievements,
        '8': rogue.unlock_all_gamemodes,
        '9': rogue.edit_vouchers,
        '10': rogue.add_candies,
        '11': rogue.edit_money,
        '12': rogue.edit_pokeballs,
        '13': rogue.edit_biome,
        '14': rogue.generate_eggs,
        '15': rogue.edit_hatchWaves,
        '16': rogue.edit_account_stats,
        '17': rogue.unlock_all_features,
        '18': rogue.create_backup,
        '19': rogue.restore_backup,
        '20': rogue.print_pokedex,
        '21': rogue.print_biomes,
        '22': rogue.print_moves,
        '23': rogue.print_vouchers,
        '24': rogue.print_natures,
        '25': rogue.print_natureSlot,
        '26': rogue.update_all,
        '27': rogue.print_help,
    }

    title = '************************ PyRogue *************************'
    working_status = '(Working)'
    broken_status = ' (Broken)'

    formatted_title = f'{Fore.GREEN}{Style.BRIGHT}{title}{Style.RESET_ALL}'
    formatted_working_status = f'{Fore.GREEN}{Style.BRIGHT}{working_status}{Style.RESET_ALL}'

    term = [
        f'{formatted_title}',
        f'1: Load Game-Data from server{' ' * 20}{formatted_working_status}',
        f'2: Load SaveSlot-Data from server{' ' * 16}{formatted_working_status}',
        f'3: Edit a starter{' ' * 32}{formatted_working_status}',
        f'4: Unlock all starters{' ' * 27}{formatted_working_status}',
        f'5: Edit your egg-tickets{' ' * 25}{formatted_working_status}',
        f'6: Edit CURRENT Pokemon Party{' ' * 20}{formatted_working_status}',
        f'7: Unlock all achievements{' ' * 23}{formatted_working_status}',
        f'8: Unlock all gamemodes{' ' * 26}{formatted_working_status}',
        f'9: Edit vouchers{' ' * 33}{formatted_working_status}',
        f'10: Add candies to a pokemon{' ' * 21}{formatted_working_status}',
        f'11: Edit money amount{' ' * 28}{formatted_working_status}',
        f'12: Edit pokeballs amount{' ' * 24}{formatted_working_status}',
        f'13: Edit biome{' ' * 35}{formatted_working_status}',
        f'14: Generate eggs{' ' * 32}{formatted_working_status}',
        f'15: Set your eggs to hatch{' ' * 23}{formatted_working_status}',
        f'16: Edit account stats{' ' * 27}{formatted_working_status}',
        f'17: Unlock Everything{' ' * 28}{formatted_working_status}',
        Fore.GREEN + Style.BRIGHT + '----------------------------------------------------------' + Style.RESET_ALL,
        f'18: Create a backup{' ' * 30}{formatted_working_status}',
        f'19: Recover your backup{' ' * 26}{formatted_working_status}',
        f'20: Show all Pokemon ID{' ' * 26}{formatted_working_status}',
        f'21: Show all Biome IDs{' ' * 27}{formatted_working_status}',
        f'22: Show all Move IDs{' ' * 28}{formatted_working_status}',
        f'23: Show all Vouchers IDs{' ' * 24}{formatted_working_status}',
        f'24: Show all Natures IDs{' ' * 25}{formatted_working_status}',
        f'25: Show all NaturesSlot IDs{' ' * 21}{formatted_working_status}',
        Fore.LIGHTYELLOW_EX + Style.BRIGHT + '-- You can always edit your trainer.json also yourself! --' + Style.RESET_ALL,
        f'26: >> Save data and upload to the Server{' ' * 2}' + Fore.LIGHTYELLOW_EX + Style.BRIGHT +'(Use when done)' + Style.RESET_ALL,
        f'27: >> Print help and program information{' ' * 17}',
        f'{formatted_title}',
    ]


    while True:
        print('')
        for line in term:
            print(Fore.GREEN + '* ' + Style.RESET_ALL + line + Fore.GREEN + ' *' + Style.RESET_ALL)
        command = input('Command: ')

        if command in func:
            func[command]()
        elif command == 'exit':
            quit()
        else:
            cFormatter.print(Color.INFO, 'Command not found.')
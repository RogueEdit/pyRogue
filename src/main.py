# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 06.06.2024 
import signal
import getpass
import requests
import brotli
from modules.loginLogic import loginLogic, HeaderGenerator
from modules.mainLogic import Rogue
from colorama import Fore, Style, init
from modules.login.seleniumLogic import SeleniumLogic
from utilities.cFormatter import cFormatter, Color
from utilities.logger import CustomLogger
import modules.config
import atexit

init()
logger = CustomLogger()

def main():
    """
    Main script execution for user login and session initialization.

    This script prompts the user for a username and password, attempts to log in,
    and if successful, initializes a PokeRogue session.

    Workflow:
        1. Ask the user if requests or selenium
        2. Initializes either a requests session
        2. or a Selenium session
        3. Prompts the user for username and password.
        4. Attempts to log in using the provided credentials.
        5. If login is successful, prints a success message and breaks the loop.
        6. If login fails, prints an error message and re-prompts the user.
        7. Handles any exceptions that occur during the login process.

    Usage:
        Run the script directly to initiate the login process:
        $ python main.py

    Modules:
        - requests: For session handling.
        - getpass: For securely obtaining the password.
        - customLogger: Custom logging functionality.
        - loginLogic: Handles the login logic.
        - login.seleniumLogic: Handles logging in with selenium
        - rogue: Initializes the PokeRogue session.
        - cFormatter: Custom formatter for colored printing and logging.
        - color: Our own module defining color codes.
    """
    session = requests.Session()
    while True:
        print('')
        cFormatter.print(Color.BRIGHT_GREEN, f'<pyRogue {modules.config.version}>')
        cFormatter.print(Color.BRIGHT_GREEN, 'We create base-backups on every login and further backups everytime you start or up choose so manually.')
        cFormatter.print(Color.BRIGHT_GREEN, 'In case of trouble, please refer to our GitHub. https://github.com/RogueEdit/onlineRogueEditor ')
        cFormatter.print_separators(60, '-')
        cFormatter.print(Color.CRITICAL, 'We hope to resolved some problems we had over the last days. Sorry for the inconvenience but it wasn\'t on us.')
        cFormatter.print(Color.CRITICAL, 'We hope this will stay working for a while.')
        cFormatter.print_separators(60, '-')
        cFormatter.print(Color.BRIGHT_MAGENTA, '1: Using requests.')
        cFormatter.print(Color.BRIGHT_MAGENTA, '2: Using own browser. Use when 1 doesnt work.')
        
        try:
            loginChoice = int(input('Please choose a method of logging in: '))
        except ValueError:
            cFormatter.print(Color.CRITICAL, "Invalid choice. Please enter a number.")
            continue
        
        username = input('Username: ')
        password = getpass.getpass('Password (password is hidden): ')

        if loginChoice == 1:
            login = loginLogic(username, password)
            try:
                if login.login():
                    cFormatter.print(Color.INFO, f'Logged in as: {username.capitalize()}')
                    session.cookies.set("pokerogue_sessionId", login.session_id, domain="pokerogue.net")
                    rogue = Rogue(session, login.token, login.session_id)
                    break
            except Exception as e:
                cFormatter.print(Color.CRITICAL, f'Something went wrong. {e}', isLogging=True)
        elif loginChoice == 2:
            selenium_logic = SeleniumLogic(username, password, 120)
            session_id, token, headers = selenium_logic.logic()  # Unpack three values

            if session_id and token and headers:
                cFormatter.print(Color.INFO, f'Logged in as: {username.capitalize()}')
                session.cookies.set("pokerogue_sessionId", session_id, domain="pokerogue.net")
                rogue = Rogue(session, auth_token=token, clientSessionId=session_id, headers=headers)
                break
            else:
                cFormatter.print(Color.CRITICAL, "Failed to retrieve necessary authentication data from Selenium.")
        else:
            cFormatter.print(Color.CRITICAL, "Invalid choice. Please choose a valid method.")

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
        '28': rogue.print_changes,
        '29': rogue.logout
    }

    title = '************************ PyRogue *************************'
    working_status = '(Working)'
    broken_status = ' (Broken)'
    header_status = '(Use when Broken)'

    formatted_title = f'{Fore.GREEN}{Style.BRIGHT}{title}{Style.RESET_ALL}'
    formatted_working_status = f'{Fore.GREEN}{Style.BRIGHT}{working_status}{Style.RESET_ALL}'
    formatted_header = f'{Fore.RED}{Style.BRIGHT}{header_status}{Style.RESET_ALL}'

    term = [
        f'{formatted_title}',
        f'1: Load Game-Data from server{" " * 20}{formatted_working_status}',
        f'2: Load SaveSlot-Data from server{" " * 16}{formatted_working_status}',
        f'3: Edit a starter{" " * 32}{formatted_working_status}',
        f'4: Unlock all starters{" " * 27}{formatted_working_status}',
        f'5: Edit your egg-tickets{" " * 25}{formatted_working_status}',
        f'6: Edit CURRENT Pokemon Party{" " * 20}{formatted_working_status}',
        f'7: Unlock all achievements{" " * 23}{formatted_working_status}',
        f'8: Unlock all gamemodes{" " * 26}{formatted_working_status}',
        f'9: Edit vouchers{" " * 33}{formatted_working_status}',
        f'10: Add candies to a pokemon{" " * 21}{formatted_working_status}',
        f'11: Edit money amount{" " * 28}{formatted_working_status}',
        f'12: Edit pokeballs amount{" " * 24}{formatted_working_status}',
        f'13: Edit biome{" " * 35}{formatted_working_status}',
        f'14: Generate eggs{" " * 32}{formatted_working_status}',
        f'15: Set your eggs to hatch{" " * 23}{formatted_working_status}',
        f'16: Edit account stats{" " * 27}{formatted_working_status}',
        f'17: Unlock Everything{" " * 28}{formatted_working_status}',
        Fore.GREEN + Style.BRIGHT + '----------------------------------------------------------' + Style.RESET_ALL,
        f'18: Create a backup{" " * 30}{formatted_working_status}',
        f'19: Recover your backup{" " * 26}{formatted_working_status}',
        f'20: Show all Pokemon ID{" " * 26}{formatted_working_status}',
        f'21: Show all Biome IDs{" " * 27}{formatted_working_status}',
        f'22: Show all Move IDs{" " * 28}{formatted_working_status}',
        f'23: Show all Vouchers IDs{" " * 24}{formatted_working_status}',
        f'24: Show all Natures IDs{" " * 25}{formatted_working_status}',
        f'25: Show all NaturesSlot IDs{" " * 21}{formatted_working_status}',
        Fore.LIGHTYELLOW_EX + Style.BRIGHT + '-- You can always edit your trainer.json also yourself! --' + Style.RESET_ALL,
        f'26: >> Save data and upload to the Server{" " * 2}' + Fore.LIGHTYELLOW_EX + Style.BRIGHT +'(Use when done)' + Style.RESET_ALL,
        f'27: >> Print help and program information{" " * 17}',
        f'28: >> Print changelogs{" " * 35}',
        f'{formatted_title}',
    ]

    try:
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
    except KeyboardInterrupt:
        print("Program interrupted by user.")

if __name__ == '__main__':
    main()



signal.signal(signal.SIGTERM, Rogue.logout)
signal.signal(signal.SIGINT, Rogue.logout)  # Handles Ctrl+C
signal.signal(signal.SIGQUIT, Rogue.logout) # Handles Ctrl+\
atexit.register(Rogue.logout)
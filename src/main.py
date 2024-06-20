# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 13.06.2024 
import getpass
import requests
import brotli  # noqa: F401
from modules.loginLogic import loginLogic
from modules.mainLogic import Rogue
from colorama import Fore, Style, init
from modules import seleniumLogic
from utilities.cFormatter import cFormatter, Color
from utilities.logger import CustomLogger
from modules import config
from datetime import datetime, timedelta

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
        config.check_for_updates(requests, datetime, timedelta, Style)      

        config.initialize_text()
        
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
            selenium_logic = seleniumLogic(username, password, 120)
            session_id, token, driver = selenium_logic.logic()  # Unpack three values

            if session_id and token and driver:
                cFormatter.print(Color.INFO, f'Logged in as: {username.capitalize()}')
                session.cookies.set("pokerogue_sessionId", session_id, domain="pokerogue.net")
                rogue = Rogue(session, auth_token=token, clientSessionId=session_id, driver=driver)
                break
            else:
                cFormatter.print(Color.CRITICAL, "Failed to retrieve necessary authentication data from Selenium.")
        else:
            cFormatter.print(Color.CRITICAL, "Invalid choice. Please choose a valid method.")


    useWhenDone = f'{Fore.LIGHTYELLOW_EX}(Use when Done)'
    title = f'<pyRogue {config.version}'
    term = [
        (title, 'title'),
        ('Account Actions', 'category'),
        (('Create a backup', ''), rogue.create_backup),
        (('Recover your backup', ''), rogue.restore_backup),
        (('Load Game-Data from server', ''), rogue.get_trainer_data),
        (('Load SaveSlot-Data from server', ''), rogue.get_gamesave_data),
        (('Edit account stats', ''), rogue.edit_account_stats),

        ('Trainer Data Actions', 'category'),
        (('Edit a starter', ''), rogue.edit_starter_separate),
        (('Edit your egg-tickets', ''), rogue.add_ticket),
        (('Edit candies on a starter', ''), rogue.add_candies),
        (('Edit Egg-hatch durations', ''), rogue.edit_hatchWaves),
        (('Generate eggs', ''), rogue.generate_eggs),
        (('Unlock all vouchers', ''), rogue.edit_vouchers),
        (('Unlock all starters', ''), rogue.unlock_all_starters),
        (('Unlock all achievements', ''), rogue.unlock_all_achievements),
        (('Unlock all gamemodes', ''), rogue.unlock_all_gamemodes),
        (('Unlock Everything', ''), rogue.unlock_all_features),

        ('Session Data Actions', 'category'),
        (('Edit CURRENT Pokemon Party', ''), rogue.edit_pokemon_party),
        (('Edit money amount', ''), rogue.edit_money),
        (('Edit pokeballs amount', ''), rogue.edit_pokeballs),
        (('Edit current biome', ''), rogue.edit_biome),

        ('Print game information', 'category'),
        (('Show all Pokemon ID', ''), rogue.print_pokedex),
        (('Show all Biome IDs', ''), rogue.print_biomes),
        (('Show all Move IDs', ''), rogue.print_moves),
        (('Show all Vouchers IDs', ''), rogue.print_vouchers),
        (('Show all Natures IDs', ''), rogue.print_natures),
        (('Show all NaturesSlot IDs', ''), rogue.print_natureSlot),

        ('You can always edit your JSON manually aswell!', 'helper'),
        (('Save data and upload to the Server', useWhenDone), rogue.update_all),
        (('Print help and program information', ''), rogue.print_help),
        (('Logout', ''), rogue.logout),
        (title, 'title'),
    ]

    try:
        while True:
            print('')
            valid_choices = cFormatter.initialize_menu(term)
            user_input = input("Command: ").strip().lower()
            if user_input == 'exit':
                raise KeyboardInterrupt  # Raise KeyboardInterrupt to exit the program
            
            # Handle user input
            if user_input.isdigit():
                choice_index = int(user_input)
                for idx, func in valid_choices:
                    if idx == choice_index:
                        func()  # Call the associated function
                        break
                    elif idx == 'exit':
                        KeyboardInterrupt()
                else:
                    print("Invalid selection. Please choose a valid menu option.")
            else:
                print("Invalid input. Please enter a number.")

    except KeyboardInterrupt:
        print("Program interrupted by user.")

if __name__ == '__main__':
    main()


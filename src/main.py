# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 13.06.2024
# Last Edited: 25.06.2024
# Based on: https://github.com/pagefaultgames/pokerogue/

"""
This script facilitates user login and session initialization for PokeRogue. It offers a menu-driven interface to 
perform various account and game data actions after a successful login using either requests or Selenium.

Features:
- User login through requests or Selenium.
- Various account and game data actions through a menu-driven interface.
- Custom logging and colored console output.

Modules:
- getpass: For securely obtaining the password from the user.
- requests: For handling HTTP sessions and requests.
- brotli: (Imported but not directly used in this script).
- loginLogic: Custom module for handling login logic using requests.
- Rogue: Custom module for initializing and interacting with the PokeRogue session.
- SeleniumLogic: Custom module for handling login using Selenium.
- cFormatter: Custom formatter for colored printing and logging.
- Color: Enumeration defining color codes for cFormatter.
- CustomLogger: Custom logging functionality.
- config: Custom module for configuration and update checking.
- datetime, timedelta: For date and time operations.
- colorama: For terminal text color formatting.
"""

import getpass
import requests
import brotli  # noqa: F401

from modules import requestsLogic, Rogue, SeleniumLogic, config
from modules.handler import OperationSuccessful, handle_operation_exceptions
from colorama import Fore, Style, init
from utilities import cFormatter, Color, CustomLogger
from datetime import datetime, timedelta

init()
config.f_initFolders()
logger = CustomLogger()
config.f_checkForUpdates(requests, datetime, timedelta, Style)
config.f_printWelcomeText()

# Global list for pre-command messages
pre_command_messages = []

def m_propagateMessages():
    """
    Prints messages from the global pre_command_messages list and then clears the list.
    """
    global pre_command_messages
    if pre_command_messages:
        for message in pre_command_messages:
            cFormatter.print(Color.INFO, message)
        pre_command_messages.clear()

@handle_operation_exceptions
def m_executeOptions(choice_index, valid_choices):
    m_propagateMessages()  # Print messages before executing the option
    for idx, func in valid_choices:
        if idx == choice_index:
            func()
            break
        elif idx == 'exit':
            raise KeyboardInterrupt

@handle_operation_exceptions
def m_mainMenu(rogue):
    title = f'{config.title}>'
    useWhenDone = f'{Fore.LIGHTYELLOW_EX}(Use when Done)'
    untouched = f'{Fore.LIGHTYELLOW_EX}(UNTOUCHED)'
    reworked = f'{Fore.GREEN}(REWORKED)'
    broken = f'{Fore.RED}(BROKEN)'
    term = [
        (title, 'title'),
        ('Account Actions', 'category'),
        (('Create a backup', untouched), rogue.create_backup),
        (('Recover your backup', untouched), rogue.restore_backup),
        (('Load Game-Data from server', untouched), rogue.get_trainer_data),
        (('Change save-slot to edit', reworked), rogue.f_changeSaveSlot),
        (('Edit account stats', reworked), rogue.f_editAccountStats),

        ('Trainer Data Actions', 'category'),
        (('Edit a starter', untouched), rogue.edit_starter_separate),
        (('Edit your egg-tickets', untouched), rogue.add_ticket),
        (('Edit candies on a starter', broken), rogue.f_addCandies),
        (('Edit Egg-hatch durations', reworked), rogue.f_editHatchWaves),
        (('Generate eggs', reworked), rogue.f_addEggsGenerator),
        (('Unlock all vouchers', untouched), rogue.f_editVouchers),
        (('Unlock all starters', untouched), rogue.f_unlockStarters),
        (('Unlock all achievements', untouched), rogue.f_editAchivements),
        (('Unlock all gamemodes', untouched), rogue.f_editGamemodes),
        (('Unlock Everything', 'mightwork'), rogue.f_unlockAllCombined),

        ('Session Data Actions', 'category'),
        (('Edit CURRENT Pokemon Party', untouched), rogue.edit_pokemon_party),
        (('Edit money amount', reworked), rogue.f_editMoney),
        (('Edit pokeballs amount', reworked), rogue.f_editPokeballs),
        (('Edit current biome', reworked), rogue.f_editBiome),
        (('Edit Items', untouched), rogue.f_submenuItemEditor),

        ('Print game information', 'category'),
        (('Show all Pokemon ID', reworked), rogue.print_pokedex),
        (('Show all Biome IDs', reworked), rogue.f_printBiomes),
        (('Show all Move IDs', reworked), rogue.print_moves),
        (('Show all Vouchers IDs', reworked), rogue.print_vouchers),
        (('Show all Natures IDs', reworked), rogue.print_natures),
        (('Show all NaturesSlot IDs', reworked), rogue.print_natureSlot),

        ('You can always edit your JSON manually as well!', 'helper'),
        (('Save data and upload to the Server', useWhenDone), rogue.update_all),
        (('Print help and program information', ''), config.f_printHelp),
        (('Logout', ''), rogue.logout),
        (title, 'title'),
    ]

    try:
        while True:
            validChoices = cFormatter.m_initializeMenu(term)
            userInput = input('Command: ').strip().lower()

            if userInput == 'exit':
                raise KeyboardInterrupt
            
            if userInput.isdigit():
                choiceIndex = int(userInput)
                m_executeOptions(choiceIndex, validChoices)
            else:
                cFormatter.print(Color.INFO, 'Invalid input. Please enter a number.')
    except OperationSuccessful as os:
        cFormatter.print(Color.DEBUG, f'Operation successful: {os}')
    except KeyboardInterrupt:
        cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
        exit()

@handle_operation_exceptions
def main():
    loginChoice = input('Please choose a method of logging in: ')
    loginChoice = int(loginChoice)  # Attempt to convert input to integer
    while True:
        try:
            
            if loginChoice not in [1, 2, 3]:
                cFormatter.print(Color.DEBUG, 'Please choose a valid option.')
                continue  # Prompt user again if choice is not valid
        except KeyboardInterrupt:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()
        except ValueError:
            cFormatter.print(Color.DEBUG, 'Invalid input. Please enter a number.')
            continue  # Prompt user again for input

        try:
            username = input('Username: ')
            password = getpass.getpass('Password (password is hidden): ')

            session = requests.Session()
            if loginChoice == 1:
                login = requestsLogic(username, password)
                try:
                    if login.login():
                        cFormatter.print(Color.INFO, f'Logged in as: {config.f_anonymizeName(username)}')
                        session.cookies.set('pokerogue_sessionId', login.sessionId, domain='pokerogue.net')
                        rogue = Rogue(session, login.token, login.sessionId)
                        break
                except Exception as e:
                    cFormatter.print(Color.CRITICAL, f'Something went wrong. {e}', isLogging=True)

            elif loginChoice in [2, 3]:
                try:
                    if loginChoice == 3:
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                    seleniumLogic = SeleniumLogic(username, password, 120, useScripts=(loginChoice == 3))
                    sessionId, token, driver = seleniumLogic.logic()

                    if sessionId and token and driver:
                        cFormatter.print(Color.INFO, f'Logged in as: {config.f_anonymizeName(username)}')
                        session.cookies.set('pokerogue_sessionId', sessionId, domain='pokerogue.net')
                        rogue = Rogue(session, auth_token=token, clientSessionId=sessionId, driver=driver, useScripts=(loginChoice == 3))
                        break
                    else:
                        cFormatter.print(Color.CRITICAL, 'Failed to retrieve necessary authentication data from Selenium.')
                except Exception as e:
                    cFormatter.print(Color.CRITICAL, f'Something went wrong. {e}', isLogging=True)

            else:
                cFormatter.print(Color.CRITICAL, 'Invalid choice. Please choose a valid method.')
        except KeyboardInterrupt:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()

    m_mainMenu(rogue)

if __name__ == '__main__':
    while True:
        try:
            main()
        except OperationSuccessful as os:
            cFormatter.print(Color.DEBUG, f'Operation successful: {os}')
        except KeyboardInterrupt:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()

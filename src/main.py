# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood 
# Date of release: 13.06.2024
# Last Edited: 28.06.2024
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
from modules.handler import OperationSuccessful, handle_operation_exceptions, OperationCancel, OperationSoftCancel
from colorama import Fore, Style, init
from utilities import cFormatter, Color, CustomLogger
from datetime import datetime, timedelta
from utilities import fh_printMessageBuffer
from sys import exit
from utilities import Generator
generator = Generator()
generator.generate()
init()
logger = CustomLogger()

if not config.debug:
    config.f_checkForUpdates(requests, datetime, timedelta, Style)


@handle_operation_exceptions
def m_executeOptions(choice_index, valid_choices):
    for idx, func in valid_choices:
        if idx == choice_index:
            func()
            break
        elif idx == 'exit':
            raise KeyboardInterrupt

@handle_operation_exceptions
def m_mainMenu(rogue, editOffline: bool = False):
    title = f'{config.title}>'
    useWhenDone = f'{Fore.LIGHTYELLOW_EX}(Use when Done)'
    reworked = f'{Fore.GREEN}(REWORKED)'

    term = [
        (title, 'title'),
        ('Account Actions', 'category'),
        ((f'{Fore.YELLOW}Create a backup', reworked), rogue.f_createBackup),
        ((f'{Fore.YELLOW}Recover your backup', reworked), rogue.f_restoreBackup),
        (('Load Game-Data from server', reworked), rogue.f_getGameData),
        (('Change save-slot to edit', reworked), rogue.f_changeSaveSlot),
        (('Edit account stats', reworked), rogue.f_editAccountStats),

        ('Edits', 'category'),
        ((f'{Fore.YELLOW}Create eggs', reworked), rogue.f_addEggsGenerator),
        ((f'Edit {Fore.YELLOW}Egg-hatch durations', reworked), rogue.f_editHatchWaves),
        ((f'Edit {Fore.YELLOW}egg-tickets', reworked), rogue.f_addTicket),
        ((f'Edit {Fore.YELLOW}a starter', reworked), rogue.f_editStarter),
        ((f'Edit {Fore.YELLOW}candies{Style.RESET_ALL} on a starter', reworked), rogue.f_addCandies),

        ('Unlocks', 'category'),
        ((f'Unlock {Fore.YELLOW}achievements', reworked), rogue.f_unlockAchievements),
        ((f'Unlock {Fore.YELLOW}vouchers', reworked), rogue.f_unlockVouchers),
        ((f'Unlock {Fore.YELLOW}all starters', reworked), rogue.f_unlockStarters),
        ((f'Unlock {Fore.YELLOW}all gamemodes', reworked), rogue.f_unlockGamemodes),
        ((f'Unlock {Fore.YELLOW}Everything', reworked), rogue.f_unlockAllCombined),

        ('Session Data Actions', 'category'),
        ((f'Edit {Fore.YELLOW}current Pokemon Party', reworked), rogue.f_editPokemonParty),
        ((f'Edit {Fore.YELLOW}money amount', reworked), rogue.f_editMoney),
        ((f'Edit {Fore.YELLOW}pokeballs amount', reworked), rogue.f_editPokeballs),
        ((f'Edit {Fore.YELLOW}current biome', reworked), rogue.f_editBiome),
        ((f'Edit {Fore.YELLOW}Items', reworked), rogue.f_submenuItemEditor),

        ('Print game information', 'category'),
        (('Show all Pokemon ID', reworked), rogue.legacy_pokedex),
        (('Show all Biome IDs', reworked), rogue.legacy_printBiomes),
        (('Show all Move IDs', reworked), rogue.legacy_moves),
        (('Show all Vouchers IDs', reworked), rogue.legacy_vouchers),
        (('Show all Natures IDs', reworked), rogue.legacy_natures),
        (('Show all NaturesSlot IDs', reworked), rogue.legacy_natureSlot),

        ('You can always edit your JSON manually as well!', 'helper'),
        ((f'{Fore.YELLOW}Save data and upload to the Server', useWhenDone), rogue.f_updateAllToServer),
        (('Print help and program information', ''), config.f_printHelp),
        (('Logout', ''), rogue.f_logout),
        (title, 'title'),
    ]
    if editOffline or config.debug:
        # Filter entrys that would break offline
        term = [entry for entry in term if entry[1] != rogue.f_updateAllToServer]
        term = [entry for entry in term if entry[1] != rogue.f_getGameData]
        term = [entry for entry in term if entry[1] != rogue.f_logout]
        replacement_entry = ('Offline-Edits are directly applied', 'helper')
        term = [replacement_entry if entry == ('You can always edit your JSON manually as well!', 'helper') else entry for entry in term]

    try:
        while True:
            validChoices = cFormatter.m_initializeMenu(term)
            fh_printMessageBuffer()
            userInput = input('Command: ').strip().lower()

            if userInput == 'exit':
                raise KeyboardInterrupt
            if userInput.isdigit() and int(userInput) <= len(validChoices):
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
    if config.debug:
        rogue = Rogue(requests.session(), auth_token="Invalid Auth Token", editOffline=config.debug)
        m_mainMenu(rogue)
    else:
        while True:
            try:
                config.f_printWelcomeText()
                loginChoice = int(input('Please choose a method of logging in: '))
                if loginChoice not in [1, 2, 3, 4]:
                    cFormatter.print(Color.DEBUG, 'Please choose a valid option.')
                    continue  # Prompt user again if choice is not valid

                if loginChoice != 4:
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
                    if loginChoice == 3:
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                        cFormatter.print(Color.INFO, 'Do not close your browser and do not browse in the game!')
                    seleniumLogic = SeleniumLogic(username, password, 120, useScripts=(loginChoice == 3))
                    sessionId, token, driver = seleniumLogic.logic()

                    if sessionId and token:
                        if not driver:
                            driver = None
                            print('Driver error')
                        cFormatter.print(Color.INFO, f'Logged in as: {config.f_anonymizeName(username)}')
                        session.cookies.set('pokerogue_sessionId', sessionId, domain='pokerogue.net')
                        rogue = Rogue(session, auth_token=token, clientSessionId=sessionId, driver=driver, useScripts=(loginChoice == 3))
                        break
                    else:
                        cFormatter.print(Color.CRITICAL, 'Failed to retrieve necessary authentication data from Selenium.')


                elif loginChoice == 4:
                    rogue = Rogue(session, auth_token='Invalid Auth Token', editOffline=True)
                    break

                else:
                    cFormatter.print(Color.CRITICAL, 'Invalid choice. Please choose a valid method.')

            except KeyboardInterrupt:
                exit()
        m_mainMenu(rogue, editOffline=(loginChoice == 4))

if __name__ == '__main__':
    while True:
        try:
            main()
        except OperationSuccessful as os:
            cFormatter.print(Color.DEBUG, f'Operation successful: {os}')
        except KeyboardInterrupt:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()
        except OperationCancel:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()
        except OperationSoftCancel:
            cFormatter.print(Color.DEBUG, '\nProgram interrupted by user.')
            exit()

    

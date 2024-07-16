# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Author
# Date of release: 25.06.2024 
# Last Edited: 28.06.2024

from modules.handler import OperationCancel, OperationSoftCancel
from enum import Enum
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from utilities import cFormatter, Color
from typing import Optional


@staticmethod
def fh_getChoiceInput(promptMesage: str, choices: dict, renderMenu: bool = False, zeroCancel: bool=False, softCancel:bool = False) -> str:
    """
    Args:
    - promptMesage (str): The prompt message to display.
    - choices (dict): The dictionary containing choice options.
    - renderMenu (bool): If True, render the menu with line breaks for readability.
    - zeroCancel (bool): If True, allow raise cancellation with '0' interrupting the operation and save.
    - softCancel (bool): If True, allow soft cancellation with '0' interrupting the operation but allow saving.

    Helper method to get a validated choice input from the user.

    Raises:
    - OperationCancel()
    - OperationSoftCancel()
    - ValueError()

    Returns:
    - str: The validated choice key.
    - or any Raise depending on setup.
    """
    if renderMenu:
        actions = "\n".join([f'{idx + 1}: {desc}' for idx, desc in enumerate(choices.values())])
        fullPrompt = f'{promptMesage}\n{actions}\nSelect a option (0: Cancel): '
    else:
        actions = " | ".join([f'{idx + 1}: {desc}' for idx, desc in enumerate(choices.values())])
        if zeroCancel or softCancel:
            fullPrompt = f'{promptMesage} (0: Cancel | {actions}): '
        else:
            fullPrompt = f'{promptMesage} ({actions}): '

    while True:
        userInput = input(fullPrompt).strip()
        if userInput.lower() == 'exit' or userInput.lower() == 'cancel' or userInput == '':
            raise OperationCancel()
        if userInput == '0':
            if zeroCancel:
                raise OperationCancel()
            if softCancel:
                raise OperationSoftCancel()
            
        # If no cancel or skip is requested
        if userInput.isdigit():
            idx = int(userInput) - 1
            if 0 <= idx < len(choices):
                return list(choices.keys())[idx]
            
        print(f'{userInput}')

@staticmethod
def fh_getIntegerInput(promptMessage: str, minBound: int, maxBound: int, zeroCancel: bool=False, softCancel: bool=False, allowSkip: bool=False) -> int:
    """
    Args:
    - prompt (str): The prompt message to display.
    - minBound (int): The minimum valid value.
    - maxBound (int): The maximum valid value.
    - zeroCancel (bool): If True, allow raise cancellation with '0' interrupting the operation and save.
    - softCancel (bool): If True, allow soft cancellation with '0' interrupting the operation but allow saving.
    - allowSkip (bool): If True, returns 'skip' 
    Helper method to get a validated integer input from the user.


    Raises:
    - OperationCancel()
    - OperationSoftCancel()
    - ValueError()
        
    Returns:
    - int: The validated integer input.
    - or any Raise depending on setup.
    """
    if zeroCancel:
        minBound = 0
        fullPrompt = f'{promptMessage} (0: Cancel | 1 - {maxBound} | "skip"): ' if allowSkip else f'{promptMessage} (0: Cancel | 1 - {maxBound}): '
    if softCancel: 
        minBound = 0
        fullPrompt = f'{promptMessage} (0: Save & Cancel | 1 - {maxBound} | "skip"): ' if allowSkip else f'{promptMessage} (0: Save & Cancel | 1 - {maxBound}): '
    else:
        fullPrompt = f'{promptMessage} ({minBound} - {maxBound}): '

    while True:
        userInput = input(fullPrompt).strip()
        if userInput.lower() == 'exit' or userInput.lower() == 'cancel' or userInput == '' or userInput == ' ' or userInput is None:
            raise OperationCancel()
        if userInput == '0':
            if zeroCancel:
                raise OperationCancel()
            elif softCancel:
                raise OperationSoftCancel()
        if allowSkip and userInput.lower() == 'skip':
            return 'skip'
        
        # If no cancel or skip is requested
        if userInput.isdigit():
            value = int(userInput)
            if minBound <= value <= maxBound:
                return str(value)
            
        cFormatter.print(Color.INFO, f'Invalid input: "{userInput}" - must be between {minBound} - {maxBound}')

@staticmethod
def fh_getCompleterInput(promptMessage: str, choices: dict, zeroCancel: bool = False, softCancel: bool = False, allowSkip: bool = False) -> str:
    """
    Args:
    - prompt_message (str): The prompt message to display.
    - choices (dict): A dictionary mapping input choices to their corresponding values.
    - zeroCancel (bool): If True, allow raise cancellation with '0' interrupting the operation and save.
    - softCancel (bool): If True, allow soft cancellation with '0' interrupting the operation but allow saving.

    Helper method to get input from the user with auto-completion support.

    Raises:
    - OperationSoftCancel()
    - OperationCancel()
    - ValueError()

    Returns:
    - str: The value corresponding to the validated input choice, or raises OperationCancel if the user cancels.
    - or any Raise depending on setup.
    """
    fullPrompt = f'{promptMessage}: '
    if zeroCancel or softCancel:
        fullPrompt = f'{promptMessage} (0: Cancel): '

    # Create a WordCompleter from the keys of choices dictionary
    completer = WordCompleter(choices.keys(), ignore_case=True)

    while True:
        try:
            userInput = prompt(fullPrompt, completer=completer).strip()  # Ensure prompt is the correct callable

            if userInput.lower() == 'exit' or userInput.lower() == 'cancel' or userInput == '':
                raise OperationCancel()
            if userInput == '0':
                if softCancel:
                    raise OperationSoftCancel()
                if zeroCancel:
                    raise OperationCancel()
            if allowSkip and userInput.lower() == 'skip':
                return 'skip'
            
            ## Validate the input
            if userInput in choices:
                return choices[userInput]

            # Ensure inputValue is a string
            inputValue = str(userInput).strip().lower()
            enumMember: Optional[Enum] = None
            if inputValue.isdigit():
                # Input is an ID
                enumMember = next((member for member in choices.values() if isinstance(member, Enum) and member.value == int(inputValue)))
            else:
                # Input is a name
                enumMember = next((member for member in choices.values() if isinstance(member, Enum) and member.name() == inputValue))

            if enumMember is not None:
                return enumMember
        # only except that here, this indicates invalid input for choicecompleter
        except StopIteration:
            cFormatter.print(Color.INFO, 'Invalid input.')

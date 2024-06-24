# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 06.06.2024 
# Last edited: 20.06.2024 - https://github.com/JulianStiebler/

"""
This module provides a custom logging formatter and various utility functions for enhanced console output.
It includes:
- An enumeration for ANSI color codes to allow colored logging output.
- A custom logging formatter (cFormatter) that supports colored console output and other formatting utilities.
- Functions for printing colored text, separators, and formatted text lines.
- A function for initializing and displaying a menu with numbered choices.
    
Modules:
- colorama: Provides ANSI escape sequences for colored terminal text.
- enum: Allows the creation of enumerations, a set of symbolic names bound to unique, constant values.
- logging: Provides a flexible framework for emitting log messages from Python programs.
- shutil: Includes high-level file operations such as copying and removal.
- typing: Provides support for type hints, enabling optional type checking.
- re: Provides support for regular expressions, allowing pattern matching in strings.

Workflow:
1. Define the Color enum for ANSI color codes.
2. Define the cFormatter class for custom logging formatting.
3. Implement static methods in cFormatter for printing colored text, separators, and formatted lines.
4. Implement a method for initializing and displaying a menu with numbered choices.
"""

from colorama import Fore, Style
# Provides ANSI escape sequences for colored terminal text, used for coloring console output.

from enum import Enum
# Allows the creation of enumerations, used here for defining color codes.

import logging
# Provides a flexible framework for emitting log messages, used for custom logging formatting.

import shutil
# Includes high-level file operations, used here for getting terminal width.

from typing import Optional, List, Tuple, Union
# Provides support for type hints, used for optional type checking and clarity.

import re
# Provides support for regular expressions, used for stripping ANSI color codes from text.

class Color(Enum):
    """
    Enum defining ANSI color codes for console output.
    
    Attributes:
        > These also trigger the corresponding logging level.
        CRITICAL (str): Bright red color for critical messages.
        DEBUG (str): Bright blue color for debug messages.
        ERROR (str): Red color for error messages.
        WARNING (str): Yellow color for warning messages.
        INFO (str): Bright light yellow color for informational messages.

        BLACK (str): Black color.
        RED (str): Red color.
        GREEN (str): Green color.
        YELLOW (str): Yellow color.
        BLUE (str): Blue color.
        MAGENTA (str): Magenta color.
        CYAN (str): Cyan color.
        WHITE (str): White color.
        BRIGHT_BLACK (str): Bright black color.
        BRIGHT_RED (str): Bright red color.
        BRIGHT_GREEN (str): Bright green color.
        BRIGHT_YELLOW (str): Bright yellow color.
        BRIGHT_BLUE (str): Bright blue color.
        BRIGHT_MAGENTA (str): Bright magenta color.
        BRIGHT_CYAN (str): Bright cyan color.
        BRIGHT_WHITE (str): Bright white color.
    """
    CRITICAL = Style.BRIGHT + Fore.RED
    DEBUG = Style.BRIGHT + Fore.BLUE
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Style.BRIGHT + Fore.LIGHTYELLOW_EX
    
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BRIGHT_BLACK = Style.BRIGHT + Fore.BLACK
    BRIGHT_RED = Style.BRIGHT + Fore.RED
    BRIGHT_GREEN = Style.BRIGHT + Fore.GREEN
    BRIGHT_YELLOW = Style.BRIGHT + Fore.YELLOW
    BRIGHT_BLUE = Style.BRIGHT + Fore.BLUE
    BRIGHT_MAGENTA = Style.BRIGHT + Fore.MAGENTA
    BRIGHT_CYAN = Style.BRIGHT + Fore.CYAN
    BRIGHT_WHITE = Style.BRIGHT + Fore.WHITE

class cFormatter(logging.Formatter):
    """
    A custom formatter for logging with colored console output.
    """
    LOG_LEVELS = {
        logging.CRITICAL: Color.CRITICAL,
        logging.DEBUG: Color.DEBUG,
        logging.ERROR: Color.ERROR,
        logging.WARNING: Color.WARNING,
        logging.INFO: Color.INFO,
    }

    @staticmethod
    def print(color: Color, text: str, isLogging: bool = False) -> None:
        """
        Logs the text to the console with specified color and optionally to a file.
        
        Args:
            color (Color): The color to use for formatting the text.
            text (str): The text to log.
            isLogging (bool, optional): Specifies whether the text is for logging. Defaults to False.
            
        Usage Example:
            cFormatter.print(Color.INFO, 'This is an informational message', isLogging=True)
            cFormatter.print(Color.DEBUG, 'This is a debug message')
            
        Example Output:
            [LIGHTYELLOW_EX]This is an informational message[RESET]
            [BLUE]This is a debug message[RESET]

        Modules/Librarys used:
        - logging: Used to log messages.
        - colorama: Used to apply color to text.
        """
        logger = logging.getLogger('root')
        
        if isLogging:
            # Determine the logging level based on color
            log_level = logging.INFO
            for level, col in cFormatter.LOG_LEVELS.items():
                if col == color:
                    log_level = level
                    break
            logger.log(log_level, text)

        # Format text with ANSI color codes and print to console
        color_code = color.value
        formatted_text = f'{color_code}{text}{Style.RESET_ALL}'
        print(formatted_text)

    @staticmethod
    def printSeperators(num_separators: Optional[int] = None, separator: str = '-', color: Optional[Color] = None) -> None:
        """
        Prints separators with the specified color.
        
        Args:
            num_separators (int, optional): The number of separator characters to print. If None, uses terminal width. Defaults to None.
            separator (str, optional): The character to use for separators. Defaults to '-'.
            color (Color, optional): The color to use for formatting separators. Defaults to None.
            
        Usage Example:
            cFormatter.print_separators(10, '-', Color.GREEN)
            cFormatter.print_separators(separator='-', color=Color.GREEN)
            
        Example Output:
            [GREEN]----------[RESET]
            [GREEN]---------------------------------------------[RESET]

        Modules/Librarys used:
        - shutil: Used to get the terminal width.
        - colorama: Used to apply color to text.
        """
        if num_separators is None:
            terminal_width = shutil.get_terminal_size().columns
            num_separators = terminal_width

        color_code = color.value if color else ''
        formatted_separators = f'{color_code}{separator * num_separators}{Style.RESET_ALL}'
        print(formatted_separators)

    @staticmethod
    def strip_color_codes(text: str) -> str:
        """
        Strips ANSI color codes from the text for accurate length calculations.
        
        Args:
            text (str): The text from which to strip ANSI color codes.
            
        Returns:
            str: The text without ANSI color codes.
            
        Usage Example:
            stripped_text = cFormatter.strip_color_codes('[GREEN]Text[RESET]')
            print(stripped_text)
            
        Example Output:
            Text

        Modules/Librarys used:
        - re: Used to strip ANSI color codes from text.
        """
        ansi_escape = re.compile(r'\x1b\[.*?m')
        return ansi_escape.sub('', text)

    @staticmethod
    def line_fill(line: str, helper_text: str = '', length: int = 55, fill_char: str = ' ', truncate: bool = False) -> str:
        """
        Formats a line of text to a fixed length by adding fill characters.
        
        Args:
            line (str): The main text line to format.
            helper_text (str, optional): Additional text to append. Defaults to ''.
            length (int, optional): The total length of the formatted line. Defaults to 55.
            fill_char (str, optional): The character used for filling empty space. Defaults to ' '.
            truncate (bool, optional): Whether to truncate the line if it exceeds the specified length. Defaults to False.
            
        Returns:
            str: The formatted line of text.
            
        Usage Example:
            formatted_line = cFormatter.line_fill('Main text', 'Helper text', 80, '-')
            print(formatted_line)
            
        Example Output:
            Main text-----------------------------------Helper text

        Modules/Librarys used:
        - re: Used to strip ANSI color codes from text.
        """
        stripped_line = cFormatter.strip_color_codes(line)
        stripped_helper_text = cFormatter.strip_color_codes(helper_text)
        
        total_length = len(stripped_line) + len(stripped_helper_text)
        
        if truncate and total_length > length:
            truncated_length = length - len(stripped_line) - 3  # 3 characters for "..."
            line = line[:truncated_length] + '...'
            stripped_line = cFormatter.strip_color_codes(line)
            total_length = len(stripped_line) + len(stripped_helper_text)

        fill_length = length - total_length
        fill = fill_char * fill_length
        return f"{Style.RESET_ALL}{line}{fill}{helper_text}"

    @staticmethod
    def center_text(text: str, length: int = 55, fill_char: str = ' ') -> str:
        """
        Centers a text within a given length, filling with the specified character.
        
        Args:
            text (str): The text to center.
            length (int, optional): The total length of the centered text. Defaults to 55.
            fill_char (str, optional): The character used for filling empty space. Defaults to ' '.
            
        Returns:
            str: The centered text.
            
        Usage Example:
            centered_text = cFormatter.center_text('Centered Text', 80, '-')
            print(centered_text)
            
        Example Output:
            --------------Centered Text---------------

        Modules/Librarys used:
        - re: Used to strip ANSI color codes from text.
        """
        stripped_text = cFormatter.strip_color_codes(text)
        total_length = len(stripped_text)
        if total_length >= length:
            return text[:length]
        
        fill_length = length - total_length
        front_fill = fill_char * (fill_length // 2)
        back_fill = fill_char * (fill_length - (fill_length // 2))
        if fill_char == '>':
            back_fill = '<' * (fill_length - (fill_length // 2))
        
        
        return f"{front_fill}{text}{back_fill}"

    @staticmethod
    def initialize_menu(term: List[Union[str, Tuple[str, str, Optional[str]], Tuple[str, callable]]], length: Optional[int] = 55) -> List[Tuple[int, callable]]:
        """
        Initializes and prints a menu based on the provided term list.
        
        Args:
            term (List[Union[str, Tuple[str, str, Optional[str]], Tuple[str, callable]]]): A list containing tuples and strings representing menu items.
            
        Returns:
            List[Tuple[int, callable]]: A list of tuples containing valid numbered choices and their associated functions.
            
        Usage Example:
            term = [
                (title, 'title'),
                (('Option 1', 'Description for option 1'), function1),
                (('Option 2', ''), function2),
                ('Helper text', 'helper'),
                ('Helper text', 'category'),
            ]
            valid_choices = cFormatter.initialize_menu(term)
            
        Example Output:
            * --------------------- pyRogue <v0.3> ---------------------- *
            1: Option 1                            Description for option 1
            2: Option 2                            
            * ----------------------- Helper text ----------------------- *
            
            Returns [(1, function1), (2, function2)]

        Modules/Librarys used:
        - colorama: Used to apply color to text.
        """
        valid_choices = []
        actual_idx = 1
        for item in term:
            if isinstance(item, tuple):
                if item[1] == 'helper':
                    print(Fore.GREEN + '* ' + cFormatter.center_text(f' {item[0]} ', length, '-') + f' {Fore.GREEN}*' + Style.RESET_ALL)
                elif item[1] == 'title':
                    print(Fore.GREEN + '* ' + cFormatter.center_text(f' {item[0]} ', length, '*') + f' {Fore.GREEN}*' + Style.RESET_ALL)
                elif item[1] == 'category':
                    print(Fore.LIGHTYELLOW_EX + '* ' + cFormatter.center_text(f' {item[0]} ', length, '>') + ' *' + Style.RESET_ALL)
                else:
                    text, func = item
                    line = f'{actual_idx}: {text[0]}'
                    formatted_line = cFormatter.line_fill(line, text[1], length, ' ', True)
                    print(Fore.GREEN + '* ' + formatted_line + f' {Fore.GREEN}*' + Style.RESET_ALL)
                    valid_choices.append((actual_idx, func))
                    actual_idx += 1
            else:
                print(Fore.YELLOW + '* ' + cFormatter.center_text(item, length, '*') + ' *' + Style.RESET_ALL)
        
        return valid_choices
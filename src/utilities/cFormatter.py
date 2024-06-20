# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 06.06.2024 
# Last edited: 20.06.2024 - https://github.com/JulianStiebler/

from colorama import Fore, Style
from enum import Enum
import logging
import shutil
from typing import Optional
import re

class Color(Enum):
    """
    Enum defining ANSI color codes for console output.
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
    def print_separators(num_separators: Optional[int] = None, separator: str = '-', color: Optional[Color] = None) -> None:
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
        """
        stripped_line = cFormatter.strip_color_codes(line)
        stripped_helper_text = cFormatter.strip_color_codes(helper_text)
        
        total_length = len(stripped_line) + len(stripped_helper_text)
        
        if truncate and total_length > length:
            truncated_length = length - len(stripped_helper_text) - 3  # 3 characters for "..."
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
        """
        stripped_text = cFormatter.strip_color_codes(text)
        total_length = len(stripped_text)
        
        if total_length >= length:
            return text[:length]
        
        fill_length = length - total_length
        front_fill = fill_char * (fill_length // 2)
        back_fill = fill_char * (fill_length - (fill_length // 2))
        
        return f"{front_fill}{text}{back_fill}"

    @staticmethod
    def initialize_menu(term: list) -> list:
        """
        Initializes and prints a menu based on the provided term list.
        
        Args:
            term (list): A list containing tuples and strings representing menu items.
            
        Returns:
            list: A list of tuples containing valid numbered choices and their associated functions.
            
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
        """
        valid_choices = []
        actual_idx = 1
        for item in term:
            if isinstance(item, tuple):
                if item[1] == 'helper':
                    print(Fore.GREEN + '* ' + cFormatter.center_text(f' {item[0]} ', 55, '-') + f' {Fore.GREEN}*' + Style.RESET_ALL)
                elif item[1] == 'title':
                    print(Fore.GREEN + '* ' + cFormatter.center_text(f' {item[0]} ', 55, '*') + f' {Fore.GREEN}*' + Style.RESET_ALL)
                elif item[1] == 'category':
                    print(Fore.LIGHTYELLOW_EX + '* ' + cFormatter.center_text(f' {item[0]} ', 55, '>') + f' {Fore.GREEN}*' + Style.RESET_ALL)
                else:
                    text, func = item
                    line = f'{actual_idx}: {text[0]}'
                    formatted_line = cFormatter.line_fill(line, text[1], 55, ' ', True)
                    print(Fore.GREEN + '* ' + formatted_line + f' {Fore.GREEN}*' + Style.RESET_ALL)
                    valid_choices.append((actual_idx, func))
                    actual_idx += 1
            else:
                print(Fore.YELLOW + '* ' + cFormatter.center_text(item, 55, '*') + ' *' + Style.RESET_ALL)
        
        return valid_choices
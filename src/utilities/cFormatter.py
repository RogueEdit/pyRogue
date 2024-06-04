from colorama import Fore, Style, init
from enum import Enum
import logging
import shutil

# Initialize colorama
init(autoreset=True)

class Color(Enum):
    CRITICAL = Style.BRIGHT + Fore.RED
    DEBUG = Style.BRIGHT + Fore.BLUE
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
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
    A custom formatter that adds color to text based on the specified color index.

    Attributes:
        COLORS (dict): Mapping of color index to colorama styles.

    Methods:
        print(color_index, text, isLogging=False): Prints or logs the text with color.
        print_separators(num_separators=None, separator='-', color=None): Prints separators with the specified color.

    Usage Example:
        cFormatter.print(Color.CYAN, 'This is a debug message', isLogging=True)
        # Output: [CYAN]This is a debug message[RESET]

    >>> cFormatter.print(Color.CYAN, 'This is a debug message', isLogging=True)
    [CYAN]This is a debug message[RESET]

    >>> cFormatter.print_separators(10, '-', Color.GREEN)
    [GREEN]----------[RESET]
    """

    COLORS = {color.name: color.value for color in Color}

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified log record as text. Adds color to the log level name if specified.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log record.
        """
        color_name = record.levelname.upper()
        if color_name in self.COLORS:
            color_code = self.COLORS[color_name]
            formatted_message = f"{color_code}{record.msg}{Style.RESET_ALL}"
            record.msg = formatted_message
        return super().format(record)

    @staticmethod
    def print(color: Color, text: str, isLogging: bool = False) -> None:
        """
        Logs the text to the file without color.

        Args:
            color (Color): The color index to use for formatting.
            text (str): The text to log.
            isLogging (bool, optional): Specifies whether the text is for logging. Defaults to False.
        """
        if isLogging:
            logger = logging.getLogger(__name__)
            logger.info(text)  # Log to file without color
        else:
            color_code = color.value
            formatted_text = f"{color_code}{text}{Style.RESET_ALL}"
            print(formatted_text)  # Print to console with color

    @staticmethod
    def print_separators(num_separators: int = None, separator: str = '-', color: Color = None) -> None:
        """
        Prints separators with the specified color.

        Args:
            num_separators (int, optional): The number of separators to print. If None, uses the terminal width. Defaults to None.
            separator (str, optional): The character used for the separators. Defaults to '-'.
            color (Color, optional): The color to use for the separators. Defaults to None.
        """
        if num_separators is None:
            terminal_width = shutil.get_terminal_size().columns
            num_separators = terminal_width

        color_code = color.value if color else ''
        formatted_separators = f"{color_code}{separator * num_separators}{Style.RESET_ALL}"
        print(formatted_separators)

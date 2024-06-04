from colorama import Fore, Style, init
from enum import Enum
import logging
import shutil


class Color(Enum):
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

class Color(Enum):
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

class Color(Enum):
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

class Color(Enum):
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
    A custom formatter that adds color to text based on the specified color index.
    """
    LOG_LEVELS = {
        logging.CRITICAL: Color.CRITICAL,
        logging.DEBUG: Color.DEBUG,
        logging.ERROR: Color.ERROR,
        logging.WARNING: Color.WARNING,
        logging.INFO: Color.INFO,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified log record as text. Adds color to the log level name if specified.
        Args:
            record (logging.LogRecord): The log record to format.
        Returns:
            str: The formatted log record.
        """
        color = self.LOG_LEVELS.get(record.levelno, Color.WHITE)
        color_code = color.value
        record.msg = f'{color_code}{record.msg}{Style.RESET_ALL}'
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
        logger = logging.getLogger(__name__)
        if isLogging:
            # Determine the logging level based on color
            for level, col in cFormatter.LOG_LEVELS.items():
                if col == color:
                    logger.log(level, text)
                    return
            logger.info(text)  # Default log level if no match
        else:
            color_code = color.value
            formatted_text = f'{color_code}{text}{Style.RESET_ALL}'
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
        formatted_separators = f'{color_code}{separator * num_separators}{Style.RESET_ALL}'
        print(formatted_separators)
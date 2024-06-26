# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 06.06.2024 
# Last Edited: 20.06.2024

"""
Online Rogue Editor Update Checker and Initialization

This script checks for updates on a GitHub repository and initializes necessary directories
for logging and backups if they do not already exist.

Modules:
- requests: HTTP library for sending GET and POST requests to GitHub's API.
- datetime: Provides classes for manipulating dates and times.
- timedelta: Represents a duration, the difference between two dates or times.
- utilities.cFormatter: Custom formatter for printing colored console output.
- os: Provides functions for interacting with the operating system, such as creating directories.

Workflow:
1. Initialize necessary directories (logs, backups, data) if they do not exist.
2. Check for updates on the GitHub repository using `check_for_updates` function.
3. Print initialization messages and helpful information using `initialize_text` and `print_help` functions.
"""

import os
from datetime import datetime, timedelta
import requests
from utilities import cFormatter, Color

debug: bool = True
debugDeactivateBackup: bool = True if debug else False
debugEnableTraceback: bool = True if debug else False
useCACERT = False if debug else os.path.join(os.getcwd(), './data/cacert.pem')
version: str = 'v0.3.3-wip'
title: str = f'<(^.^(< pyRogue {version} >)^.^)>'
owner: str = 'rogueEdit'
repo: str = 'onlineRogueEditor'
repoURL: str = f'https://github.com/{owner}/{repo}/'
releaseDate: str = '23.06.2024 10:30'

logsDirectory: str = os.path.join(os.getcwd(), 'logs')
backupDirectory: str = os.path.join(os.getcwd(), 'backups')
dataDirectory: str = os.path.join(os.getcwd(), 'data')

def f_checkForUpdates(requests: requests, datetime: datetime, timedelta: timedelta, Style: object) -> None:
    """
    Check for updates on the GitHub repository since a specified release date.

    Args:
        requests (requests): HTTP library for sending requests to GitHub's API.
        datetime (datetime): Module for date and time manipulation.
        timedelta (timedelta): Represents a duration, the difference between two dates or times.
        Style (object): Object representing a formatting style (not used in this function).

    Usage Example:
        >>> check_for_updates(requests, datetime, timedelta, Style)

    Output Example:
        - Prints commit details if updates are found.
        - Provides a URL to view the latest code.
        - Advises updating the source code if updates are found.

    Modules/Librarys used and for what purpose exactly in each function:
    - requests: Sends HTTP GET requests to retrieve commit history from GitHub repository.
    - datetime: Converts release date to ISO 8601 format for GitHub API query.
    - timedelta: Calculates local timezone offset for converting release date to UTC.
    - utilities.cFormatter: Prints colored console output for displaying update details.
    """
    def f_convertToISOFormat(date_string: str, timedelta: timedelta) -> str:
        """
        Convert a date string to ISO 8601 format in UTC timezone.

        Args:
            date_string (str): Date string in format 'dd.mm.yyyy HH:MM'.
            timedelta (timedelta): Represents a duration, the difference between two dates or times.

        Returns:
            str: ISO 8601 formatted date string in UTC timezone.

        Raises:
            ValueError: If the input date format is incorrect.

        Usage Example:
            >>> convert_to_iso_format('20.06.2024 6:00', timedelta)

        Modules/Librarys used and for what purpose exactly in each function:
        - datetime: Parses and formats the input date string.
        """
        # Parse the input date string
        dateFormat = '%d.%m.%Y %H:%M'
        try:
            dt = datetime.strptime(date_string, dateFormat)
        except ValueError as e:
            raise ValueError("Incorrect date format, should be 'dd.mm.yyyy HH:MM'") from e

        # Determine local timezone offset for Central European Time (CET)
        isDST = datetime.now().timetuple().tm_isdst
        timezoneOffset = timedelta(hours=2) if isDST else timedelta(hours=1)

        # Apply local timezone offset to convert to UTC
        utcDT = dt - timezoneOffset

        # Format datetime object to ISO 8601 format with UTC timezone 'Z' (Zulu time)
        isoFormat = utcDT.strftime('%Y-%m-%dT%H:%M:%SZ')

        return isoFormat

    try:
        # Convert release date to ISO 8601 format
        check_date = datetime.fromisoformat(f_convertToISOFormat(releaseDate, timedelta))

        # Construct GitHub API URL and parameters
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        params = {'since': check_date.isoformat()}

        # Send GET request to GitHub API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        commits = response.json()  # Parse JSON response

        # Extract commit titles and SHAs
        commitList = [{'sha': commit['sha'], 'message': commit['commit']['message']} for commit in commits]

        if commitList:
            cFormatter.print(Color.CRITICAL, '********* Outdated source code found. New commits: *********')
            for commit in commitList:
                cFormatter.print(Color.WARNING, f'---- Commit Name: ({commit["message"]})')
                cFormatter.print(Color.CYAN, f'------> with SHA ({commit["sha"]})')
            cFormatter.print(Color.INFO, f'You can view the latest code here: {repoURL}')
            cFormatter.print(Color.INFO, 'It is highly recommended to update the source code. Some things might not be working as expected.')
            cFormatter.fh_printSeperators(60, '-', Color.CRITICAL)
        else:
            cFormatter.print(Color.GREEN, 'No updates found.')

    except ValueError as ve:
        cFormatter.print(Color.CRITICAL, f'Couldnt resolve check_for_updates() - ValueError occurred: {ve}')
    except requests.exceptions.RequestException as re:
        cFormatter.print(Color.CRITICAL, f'Couldnt resolve check_for_updates() - RequestException occurred: {re}')
    except Exception as e:
        cFormatter.print(Color.CRITICAL, f'Couldnt resolve check_for_updates() - An unexpected error occurred: {e}')

def f_printWelcomeText() -> None:
    """
    Print initialization messages for the program.

    This function prints messages regarding program initialization, network settings, and program version.

    Usage Example:
        >>> initialize_text()

    Modules/Librarys used and for what purpose exactly in each function:
    - utilities.cFormatter: Prints colored console output for initialization messages.
    """
    cFormatter.print(Color.BRIGHT_GREEN, f'<pyRogue {version}>')
    cFormatter.print(Color.BRIGHT_GREEN, 'We create base-backups on every login and further backups every time you start or choose so manually.')
    cFormatter.print(Color.BRIGHT_GREEN, 'In case of trouble, please switch your Network (Hotspot, VPN etc).')
    cFormatter.print(Color.BRIGHT_GREEN, f'Otherwise please visit {repoURL} and report the issue.')
    cFormatter.fh_printSeperators(60, '-')
    cFormatter.print(Color.BRIGHT_MAGENTA, '1: Using no browser with requests.    Reliability 6/10')
    cFormatter.print(Color.BRIGHT_MAGENTA, '2: Using own browser with requests.   Reliability 7/10')
    cFormatter.print(Color.BRIGHT_MAGENTA, '3: Using own browser with JavaScript. Reliability 9/10')
    cFormatter.print(Color.BRIGHT_MAGENTA, '4: Just edit an existing trainer.json')

def f_printHelp() -> None:
    """
    Print helpful information for the user.

    This function prints various helpful messages for the user, including information
    about manual JSON editing, assistance through the program's GitHub page, release
    version details, and cautions about account safety and program authenticity.

    Usage Example:
        >>> print_help()

    Modules/Librarys used and for what purpose exactly in each function:
    - utilities.cFormatter: Prints colored console output for help messages.
    """
    cFormatter.print(Color.INFO, 'You can always edit your JSON manually as well.')
    cFormatter.print(Color.INFO, 'If you need assistance, please refer to the program\'s GitHub page.')
    cFormatter.print(Color.INFO, f'{repoURL}')
    cFormatter.print(Color.INFO, f'This is release version {version} - please include that in your issue or question report.')
    cFormatter.print(Color.INFO, 'This version now also features a log file.')
    cFormatter.print(Color.INFO, 'We do not take responsibility if your accounts get flagged or banned, and')
    cFormatter.print(Color.INFO, 'you never know if there is a clone of this program. If you are not sure, please')
    cFormatter.print(Color.INFO, 'calculate the checksum of this binary and visit {repo_url}')
    cFormatter.print(Color.INFO, 'to see the value it should have to know it\'s original from source.')

def f_initFolders() -> None:
    """
    Initialize necessary directories for logs, backups, and data.

    This function checks if necessary directories (logs, backups, data) exist and creates them if they do not.

    Usage Example:
        >>> initialize_folders()

    Modules/Librarys used and for what purpose exactly in each function:
    - os: Interacts with the operating system to create directories.
    """

    # Create the logs directory if it doesn't exist
    if not os.path.exists(logsDirectory):
        os.makedirs(logsDirectory)
        cFormatter.print(Color.GREEN, f'Created logs directory: {logsDirectory}')
    # Create the backups directory if it doesn't exist
    if not os.path.exists(backupDirectory):
        os.makedirs(backupDirectory)
        cFormatter.print(Color.GREEN, f'Created backup directory: {backupDirectory}')

def f_anonymizeName(username):
    if len(username) < 3:  # If username length is less than 3, return as is (minimum 2 characters)
        return username
    
    visibleChars = max(int(len(username) * 0.2), 1)  # Calculate how many characters to leave visible
    startVisible = max(visibleChars // 2, 1)  # At least 1 character visible from the start
    endVisible = visibleChars - startVisible  # Remaining visible characters from the end
    
    # Construct the masked username
    maskedUsername = username[:startVisible] + '*' * (len(username) - startVisible - endVisible)
    
    return maskedUsername
    
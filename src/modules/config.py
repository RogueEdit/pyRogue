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
from utilities.cFormatter import cFormatter, Color

version: str = 'v0.3'
owner: str = 'rogueEdit'
repo: str = 'onlineRogueEditor'
repo_url: str = f'https://github.com/{owner}/{repo}/'
release_date: str = '20.06.2024 6:00'

logs_directory: str = os.path.join(os.getcwd(), 'logs')
backups_directory: str = os.path.join(os.getcwd(), 'backups')
data_directory: str = os.path.join(os.getcwd(), 'data')

def check_for_updates(requests: requests, datetime: datetime, timedelta: timedelta, Style: object) -> None:
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
    def convert_to_iso_format(date_string: str, timedelta: timedelta) -> str:
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
        date_format = '%d.%m.%Y %H:%M'
        try:
            dt = datetime.strptime(date_string, date_format)
        except ValueError as e:
            raise ValueError("Incorrect date format, should be 'dd.mm.yyyy HH:MM'") from e

        # Determine local timezone offset for Central European Time (CET)
        is_dst = datetime.now().timetuple().tm_isdst
        timezone_offset = timedelta(hours=2) if is_dst else timedelta(hours=1)

        # Apply local timezone offset to convert to UTC
        utc_dt = dt - timezone_offset

        # Format datetime object to ISO 8601 format with UTC timezone 'Z' (Zulu time)
        iso_format = utc_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        return iso_format

    try:
        # Convert release date to ISO 8601 format
        check_date = datetime.fromisoformat(convert_to_iso_format(release_date, timedelta))

        # Construct GitHub API URL and parameters
        url = f'https://api.github.com/repos/{owner}/{repo}/commits'
        params = {'since': check_date.isoformat()}

        # Send GET request to GitHub API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        commits = response.json()  # Parse JSON response

        # Extract commit titles and SHAs
        commit_list = [{'sha': commit['sha'], 'message': commit['commit']['message']} for commit in commits]

        if commit_list:
            cFormatter.print(Color.CRITICAL, "********* Outdated source code found. New commits: *********")
            for commit in commit_list:
                cFormatter.print(Color.WARNING, f"---- Commit Name: ({commit['message']})")
                cFormatter.print(Color.CYAN, f"------> with SHA ({commit['sha']})")
            cFormatter.print(Color.INFO, f"You can view the latest code here: {repo_url}")
            cFormatter.print(Color.INFO, 'It is highly recommended to update the source code. Some things might not be working as expected.')
            cFormatter.print_separators(60, '-', Color.CRITICAL)
        else:
            cFormatter.print(Color.GREEN, 'No updates found.')

    except ValueError as ve:
        cFormatter.print(Color.CRITICAL, f"Couldn't resolve check_for_updates() - ValueError occurred: {ve}")
    except requests.exceptions.RequestException as re:
        cFormatter.print(Color.CRITICAL, f"Couldn't resolve check_for_updates() - RequestException occurred: {re}")
    except Exception as e:
        cFormatter.print(Color.CRITICAL, f"Couldn't resolve check_for_updates() - An unexpected error occurred: {e}")

def initialize_text() -> None:
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
    cFormatter.print(Color.BRIGHT_GREEN, f'Otherwise please visit {repo_url} and report the issue.')
    cFormatter.print_separators(60, '-')
    cFormatter.print(Color.BRIGHT_MAGENTA, '1: Using no browser with requests.   Reliability 5/10')
    cFormatter.print(Color.BRIGHT_MAGENTA, '2: Using own browser with requests.   Reliability 7/10')
    cFormatter.print(Color.BRIGHT_MAGENTA, '3: Using own browser with JavaScript. Reliability 9/10')

def print_help() -> None:
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
    cFormatter.print(Color.INFO, f'{repo_url}')
    cFormatter.print(Color.INFO, f'This is release version {version} - please include that in your issue or question report.')
    cFormatter.print(Color.INFO, 'This version now also features a log file.')
    cFormatter.print(Color.INFO, 'We do not take responsibility if your accounts get flagged or banned, and')
    cFormatter.print(Color.INFO, 'you never know if there is a clone of this program. If you are not sure, please')
    cFormatter.print(Color.INFO, 'calculate the checksum of this binary and visit {repo_url}')
    cFormatter.print(Color.INFO, 'to see the value it should have to know it\'s original from source.')

def initialize_folders() -> None:
    """
    Initialize necessary directories for logs, backups, and data.

    This function checks if necessary directories (logs, backups, data) exist and creates them if they do not.

    Usage Example:
        >>> initialize_folders()

    Modules/Librarys used and for what purpose exactly in each function:
    - os: Interacts with the operating system to create directories.
    """

    # Create the logs directory if it doesn't exist
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
        cFormatter.print(Color.GREEN, f'Created logs directory: {logs_directory}')
    # Create the backups directory if it doesn't exist
    if not os.path.exists(backups_directory):
        os.makedirs(backups_directory)
        cFormatter.print(Color.GREEN, f'Created backup directory: {backups_directory}')
    # Create the backups directory if it doesn't exist
    if not os.path.exists(data_directory):
        os.makedirs(backups_directory)
        cFormatter.print(Color.GREEN, f'Created backup directory: {backups_directory}')
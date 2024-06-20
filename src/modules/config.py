from utilities.cFormatter import cFormatter, Color
import os

version = 'v0.3'

#Update Notifier
# GitHub repository details
owner = 'rogueEdit'
repo = 'onlineRogueEditor'
repo_url = f'https://github.com/{owner}/{repo}/'
release_date = '20.06.2024 6:00'


logs_directory = os.path.join(os.getcwd(), 'logs')
backups_directory = os.path.join(os.getcwd(), 'backups')
data_directory = os.path.join(os.getcwd(), 'data')

def check_for_updates(requests, datetime, timedelta, Style):
    """
    Get the list of commits (titles and SHAs) since a given date on a specified branch.

    :param requests: requests module for HTTP requests
    :param datetime: datetime module for date/time handling
    :param timedelta: timedelta module for timedelta calculations
    """
    repo_url = f'https://github.com/{owner}/{repo}'  # Assuming you define these somewhere

    def convert_to_iso_format(date_string, timedelta):
        """
        Convert a date string from format 'dd.mm.yyyy HH:MM' to ISO 8601 format 'YYYY-MM-DDTHH:MM:SSZ' in UTC timezone.

        :param date_string: Date string in format 'dd.mm.yyyy HH:MM'
        :return: ISO 8601 formatted date string in UTC timezone
        """
        # Parse the input date string
        date_format = '%d.%m.%Y %H:%M'
        try:
            dt = datetime.strptime(date_string, date_format)
        except ValueError as e:
            raise ValueError("Incorrect date format, should be 'dd.mm.yyyy HH:MM'") from e

        # Define the local timezone offset for Central European Time (CET)
        # During daylight saving time (CEST), the offset is UTC+2
        # During standard time (CET), the offset is UTC+1
        # Adjust this offset as needed based on the current date
        is_dst = datetime.now().timetuple().tm_isdst
        if is_dst:
            timezone_offset = timedelta(hours=2)
        else:
            timezone_offset = timedelta(hours=1)

        # Apply the local timezone offset to convert to UTC
        utc_dt = dt - timezone_offset

        # Format datetime object to ISO 8601 format with UTC timezone 'Z' (Zulu time)
        iso_format = utc_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

        return iso_format

    try:
        # Convert fixed date to datetime object
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
            cFormatter.print(Color.CRITICAL, "********* Outdated sourcecode found. New commits: *********", isLogging=True)
            for commit in commit_list:
                cFormatter.print(Color.WARNING, f"---- Commit Name: ({commit['message']})", isLogging=True)
                cFormatter.print(Color.CYAN, f"------> with SHA ({commit['sha']})", isLogging=True)
            cFormatter.print(Color.INFO, f"You can view the latest code here: {repo_url}")
            cFormatter.print(Color.INFO, 'It is highly recommended to update the source code. Some things might not be working as expected.')
            cFormatter.print_separators(60, '-', Color.CRITICAL)
        else:
            cFormatter.print(Color.GREEN, 'No updates found.')
    except ValueError as ve:
        cFormatter.print(Color.CRITICAL, f"Couldn\'t resolve check_for_updates() - ValueError occurred: {ve}", isLogging=True)
    except requests.exceptions.RequestException as re:
        cFormatter.print(Color.CRITICAL, f"Couldn\'t resolve check_for_updates() - RequestException occurred: {re}", isLogging=True)
    except Exception as e:
        cFormatter.print(Color.CRITICAL, f"Couldn\'t resolve check_for_updates() - An unexpected error occurred: {e}", isLogging=True)

def initialize_text():
    cFormatter.print(Color.BRIGHT_GREEN, f'<pyRogue {version}>')
    cFormatter.print(Color.BRIGHT_GREEN, 'We create base-backups on every login and further backups everytime you start or up choose so manually.')
    cFormatter.print(Color.BRIGHT_GREEN, f'In case of trouble, please switch your Network (Hotspot, VPN etc). \nOtherwise please visit {repo_url} and report the issue.')
    cFormatter.print_separators(60, '-')
    cFormatter.print(Color.BRIGHT_MAGENTA, '1: Using no  browser with requests.   Reliability 5/10')
    cFormatter.print(Color.BRIGHT_MAGENTA, '2: Using own browser with requests.   Reliability 7/10')
    cFormatter.print(Color.BRIGHT_MAGENTA, '3: Using own browser with javascript. Reliability 9/10')

def print_help() -> None:
    """
    Print helpful information for the user.

    This method prints various helpful messages for the user, including information
    about manual JSON editing, assistance through the program's GitHub page, release
    version details, and cautions about account safety and program authenticity.
    """
    cFormatter.print(Color.INFO, 'You can always edit your json manually aswell.')
    cFormatter.print(Color.INFO, 'If you need assistance please refer to the programs GitHub page.')
    cFormatter.print(Color.INFO, 'https://github.com/RogueEdit/onlineRogueEditor/.')
    cFormatter.print(Color.INFO, f'This is release version {version} - please include that in your issue or question report.')
    cFormatter.print(Color.INFO, 'This version now also features a log file.')
    cFormatter.print(Color.INFO, 'We do not take responsibility if your accounts get flagged or banned, and')
    cFormatter.print(Color.INFO, 'you never know if there is a clone from this programm. If you are not sure please')
    cFormatter.print(Color.INFO, 'calculate the checksum of this binary and visit https://github.com/RogueEdit/onlineRogueEditor/')
    cFormatter.print(Color.INFO, 'to see the value it should have to know its original from source.')

def initialize_folders() -> None:
    # Create the logs directory if it doesn't exist
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
        print(f'Created logs directory: {logs_directory}')
    # Create the backups directory if it doesn't exist
    if not os.path.exists(backups_directory):
        os.makedirs(backups_directory)
        print(f'Created backup directory: {backups_directory}')
    # Create the backups directory if it doesn't exist
    if not os.path.exists(data_directory):
        os.makedirs(backups_directory)
        print(f'Created backup directory: {backups_directory}')
from utilities.cFormatter import cFormatter, Color

version = 'v0.2.3'

#Update Notifier
# GitHub repository details
owner = 'rogueEdit'
repo = 'onlineRogueEditor'
repo_url = f'https://github.com/{owner}/{repo}/'
<<<<<<< Updated upstream
release_date = '20.06.2024 5:43'
=======
release_date = '20.06.2024 5:50'
>>>>>>> Stashed changes



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
    except ValueError as ve:
        cFormatter.print(Color.CRITICAL, f"Couldn\'t resolve check_for_updates() - ValueError occurred: {ve}", isLogging=True)
    except requests.exceptions.RequestException as re:
        cFormatter.print(Color.CRITICAL, f"Couldn\'t resolve check_for_updates() - RequestException occurred: {re}", isLogging=True)
    except Exception as e:
        cFormatter.print(Color.CRITICAL, f"Couldn\'t resolve check_for_updates() - An unexpected error occurred: {e}", isLogging=True)

def initialize_text():
    cFormatter.print(Color.BRIGHT_GREEN, f'<pyRogue {version}>')
    cFormatter.print(Color.BRIGHT_GREEN, 'We create base-backups on every login and further backups everytime you start or up choose so manually.')
    cFormatter.print(Color.BRIGHT_GREEN, f'In case of trouble, please refer to our GitHub. {repo_url}')
    cFormatter.print_separators(60, '-')
    cFormatter.print(Color.BRIGHT_MAGENTA, '1: Using requests.')
    cFormatter.print(Color.BRIGHT_MAGENTA, '2: Using own browser. Use when 1 doesnt work.')


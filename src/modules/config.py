from utilities.cFormatter import cFormatter, Color

version = 'v0.2.3'

#Update Notifier
# GitHub repository details
owner = 'rogueEdit'
repo = 'onlineRogueEditor'
branch = 'update-notifier-test'  # Specify the branch name here
repo_url = f'https://github.com/{owner}/{repo}/tree/{branch}'
release_date = '20.06.2024 5:00'



def check_for_updates(requests, datetime, timedelta):
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
        params = {'sha': branch, 'since': check_date.isoformat()}

        # Send GET request to GitHub API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        commits = response.json()  # Parse JSON response

        # Extract commit titles and SHAs
        commit_list = [{'sha': commit['sha'], 'message': commit['commit']['message']} for commit in commits]

        if commit_list:
            print(f"New commits found on branch '{branch}':")
            for commit in commit_list:
                print(f"- {commit['message']} ({commit['sha']})")
            print(f"You can view the latest code here: {repo_url}")
            input('It is highly recommended to update the source code.')
        else:
            print('No new commits on GitHub. No updates found.')

    except ValueError as ve:
        print(f"ValueError occurred: {ve}")
        # Handle incorrect date format or other value errors gracefully
    except requests.exceptions.RequestException as re:
        print(f"RequestException occurred: {re}")
        # Handle request exceptions (e.g., connection errors) gracefully
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Handle any unexpected exceptions to prevent crashing

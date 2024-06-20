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

    :param owner: Repository owner
    :param repo: Repository name
    :param branch: Branch name
    :param since_date: datetime object representing the fixed date
    :return: list of dictionaries containing commit SHA and commit message
    """
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
        except ValueError:
            raise ValueError("Incorrect date format, should be 'dd.mm.yyyy HH:MM'")

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
    # Convert fixed date to datetime object
    check_date = datetime.fromisoformat(convert_to_iso_format(release_date, timedelta))

    url = f'https://api.github.com/repos/{owner}/{repo}/commits'
    params = {'sha': branch, 'since': check_date.isoformat()}
    response = requests.get(url, params=params)
    response.raise_for_status()
    commits = response.json()

    # Extract commit titles and SHAs
    commit_list = [{'sha': commit['sha'], 'message': commit['commit']['message']} for commit in commits]

    if commit_list:
        print(f"New commits found on branch '{branch}':")
        for commit in commit_list:
            print(f"- {commit['message']} ({commit['sha']})")
        print(f"You can view the latest code here: {repo_url}")
        input('It is highly recommended to update the source code.')
    else:
        cFormatter.print(Color.GREEN, 'No new commits on GitHub. No updates found.')

# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 05.06.2024 

import os
import json
from utilities.cFormatter import cFormatter, Color
import requests
from utilities.headers import user_agents, header_languages
import random
from colorama import init
from typing import List, Dict

init()

class HeaderGenerator:
    retry_count = 0
    headerfile = './data/headerfile-save'
    headerfile_public = './data/headerfile-public'
    git_url = 'https://raw.githubusercontent.com/RogueEdit/.github/main/headergen-data'
    extra_file_path = 'data/extra.json'

    if os.path.exists(headerfile_public):
        with open(headerfile_public, 'r') as f:
            headers = f.read()
            exec(headers)
    else:
        response = requests.get(git_url)
        if response.status_code == 200:
            headers_response = response.text
            with open(headerfile_public, 'w') as f:
                f.write(headers_response)
            with open(headerfile, 'r') as f:
                headers = f.read()
                exec(headers)

    @classmethod
    def generate_user_agent(cls, os: str, browser: str) -> str:
        """
        Generate a User-Agent string based on the given operating system and browser.

        Args:
            os (str): The operating system to be used in the User-Agent string.
            browser (str): The browser to be used in the User-Agent string.

        Returns:
            str: A formatted User-Agent string.

        Example:
            >>> HeaderGenerator.generate_user_agent("Windows NT 10.0", "Chrome")
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        """
        return f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/88.0.4324.150 Safari/537.36"

    @classmethod
    def generate_headers(cls, auth_token: str = None) -> Dict[str, str]:
        """
        Generate randomized but valid HTTP headers including a User-Agent string.

        Args:
            auth_token (str, optional): An optional authorization token to include in the headers.

        Returns:
            Dict[str, str]: A dictionary containing HTTP headers.

        Example:
            >>> headers = HeaderGenerator.generate_headers()
            >>> "User-Agent" in headers
            True
        """
        device = random.choice(list(cls.operating_systems.keys()))
        os = random.choice(cls.operating_systems[device])
        browser = random.choice(cls.browsers)
        user_agent = cls.generate_user_agent(os, browser)

        headers = cls.static_headers.copy()
        headers.update({
            "User-Agent": user_agent,
            "Sec-Ch-Ua-Platform": cls.platforms[device],
        })

        if auth_token:
            headers["Authorization"] = auth_token

        return headers
    
    @classmethod
    def read_403_count(cls):
        """Read the 403 error count from the extra.json file."""
        if not os.path.exists(cls.extra_file_path):
            return 0
        with open(cls.extra_file_path, 'r') as f:
            data = json.load(f)
            return data.get('total_403_errors', 0)

    @classmethod
    def write_403_count(cls, count):
        """Write the 403 error count to the extra.json file."""
        if os.path.exists(cls.extra_file_path):
            with open(cls.extra_file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        data['total_403_errors'] = count
        with open(cls.extra_file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    @classmethod
    def handle_dynamic_header_data(cls, force_fetch=False):
        """
        Handle regeneration of header data in case of 403 error.

        Regenerate a header and save it in the headerfile-save. If this method is called 
        three times, delete the headerfile-save and refetch the data from the remote source.
        If force_fetch is True, directly fetch the header data from the remote source.
        Count the total number of 403 errors.
        """
        total_403_errors = cls.read_403_count()

        if force_fetch or total_403_errors >= 3:
            cls.retry_count = 3  # Set retry_count to 3 to force fetch
        
        cls.retry_count += 1

        # Always delete the existing header file
        if os.path.exists(cls.headerfile):
            os.remove(cls.headerfile)

        if cls.retry_count < 3:
            headers = cls.generate_headers()
            with open(cls.headerfile, 'w') as f:
                f.write(str(headers))
            cFormatter.print(Color.INFO, 'Headers regenerated and saved.', isLogging=True)
            cFormatter.print(Color.INFO, f'If the errors persist, please retry {3 - cls.retry_count} more times.', isLogging=True)
        else:
            response = requests.get(cls.git_url)
            if response.status_code == 200:
                headers_response = response.headers  # Use response.headers instead of response.text
                with open(cls.headerfile, 'w') as f:
                    f.write(str(headers_response))
                with open(cls.headerfile_public, 'w') as f:
                    f.write(response.text)
                cFormatter.print(Color.WARNING, 'Fetched new header data from remote source.', isLogging=True)
            cls.retry_count = 0  # Reset the counter
            total_403_errors += 1  # Increment the total 403 error count
            cls.write_403_count(total_403_errors)
        
        cFormatter.print(Color.INFO, 'Headers refetched restart the tool.')
        cFormatter.print(Color.INFO, f'Total number of 403 errors encountered: {total_403_errors}', isLogging=True)
        
        # Reset total_403_errors in the JSON file after 3 retries or force fetch
        if cls.retry_count == 0 or total_403_errors >= 3:
            cls.write_403_count(0)

class loginLogic:
    """
    A class to handle login logic for pokerogue.net API.

    Attributes:
        LOGIN_URL (str): The URL for the login endpoint.
        username (str): The username for login.
        password (str): The password for login.
        token (str): The authentication token retrieved after successful login.
        session_id (str): The session ID obtained after successful login.
        session (requests.Session): The session object for making HTTP requests.
    """
    LOGIN_URL = 'https://api.pokerogue.net/account/login'

    def __init__(self, username: str, password: str) -> None:
        """
        Initializes the loginLogic object.

        Args:
            username (str): The username for login.
            password (str): The password for login.
        """
        self.username = username
        self.password = password
        self.token = None
        self.session_id = None
        self.session = requests.Session()


    def login(self) -> bool:
        """
        Logs in via the pokerogue.net API.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        data = {'username': self.username, 'password': self.password}
        try:
            # Generate headers, utilizing the saved header file if it exists
            headers = HeaderGenerator.generate_headers()

            # Make the POST request with the generated headers
            response = self.session.post(self.LOGIN_URL, headers=headers, data=data)
            response.raise_for_status()

            # Process the response
            login_response = response.json()
            self.token = login_response.get('token')
            cFormatter.print_separators(30, '-')
            cFormatter.print(Color.GREEN, f'Login successful.')
            if self.token:
                cFormatter.print(Color.CYAN, f'Token: {self.token}')
            
            # Determine color based on response status code
            status_code_color = Color.BRIGHT_GREEN if response.status_code == 200 else Color.BRIGHT_RED
            cFormatter.print(status_code_color, f'HTTP Status Code: {response.status_code}', isLogging=True)
            cFormatter.print(Color.CYAN, f'Response URL: {response.request.url}', isLogging=True)
            cFormatter.print(Color.CYAN, f'Response Headers: {response.request.headers}', isLogging=True)

            # Filter and print response headers
            filtered_headers = {key: value for key, value in response.headers.items() if key != 'Report-To'}
            cFormatter.print(Color.CYAN, f'Response Headers: {filtered_headers}')
            cFormatter.print(Color.CYAN, f'Response Body: {response.text}', isLogging=True)
            cFormatter.print_separators(30, '-')
            
            return True

        except requests.RequestException as e:
            # Handle any request exceptions
            cFormatter.print(Color.CRITICAL, f'Login failed. {e}', isLogging=True)
            return False
# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 05.06.2024 

from utilities.cFormatter import cFormatter, Color
import requests
from utilities.headers import user_agents, header_languages
import random
from colorama import init

init()

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

    def _generate_headers(self) -> dict:
        """
        Generates HTTP headers for requests.

        Returns:
            dict: A dictionary containing HTTP headers.
        """
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/x-www-form-urlencoded',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': random.choice(header_languages),
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://pokerogue.net/',
            'content-encoding': 'br',
            'Origin': 'https://pokerogue.net/',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty'
        }
        return headers

    def login(self) -> bool:
        """
        Logs in to the pokerogue.net API.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        data = {'username': self.username, 'password': self.password}
        try:
            headers = self._generate_headers()
            response = self.session.post(self.LOGIN_URL, headers=headers, data=data)
            response.raise_for_status()
            login_response = response.json()
            self.token = login_response.get('token')
            cFormatter.print_separators(30, '-')
            cFormatter.print(Color.GREEN, f'Login successful.')
            if self.token:
                cFormatter.print(Color.CYAN, f'Token: {self.token}')
            status_code_color = Color.BRIGHT_GREEN if response.status_code == 200 else Color.BRIGHT_RED
            cFormatter.print(status_code_color, f'HTTP Status Code: {response.status_code}', isLogging=True)
            cFormatter.print(Color.CYAN, f'Response URL: {response.request.url}', isLogging=True)
            cFormatter.print(Color.CYAN, f'Response Headers: {response.request.headers}', isLogging=True)
            filtered_headers = {key: value for key, value in response.headers.items() if key != 'Report-To'}
            cFormatter.print(Color.CYAN, f'Response Headers: {filtered_headers}')
            cFormatter.print(Color.CYAN, f'Response Body: {response.text}', isLogging=True)
            cFormatter.print_separators(30, '-')
            return True
        except requests.RequestException as e:
            cFormatter.print(Color.CRITICAL, f'Login failed. {e}', isLogging=True)
            return False
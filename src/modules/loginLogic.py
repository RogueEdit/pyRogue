# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 04.06.2024 

from utilities.cFormatter import cFormatter, Color
import requests
from utilities.headers import user_agents, header_languages
import random
from colorama import init, Fore, Style

init()

class loginLogic:
    LOGIN_URL = 'https://api.pokerogue.net/account/login'
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.token = None
        self.session_id = None
        self.session = requests.Session()

    # General purpose header
    def _generate_headers(self) -> dict:
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
        data = {'username': self.username, 'password': self.password}
        try:
            # Generate headers dynamically using _generate_headers method
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
            cFormatter.print(Color.CYAN, f'Response URL: {response.request.url}')
            cFormatter.print(Color.CYAN, f'Response Headers: {response.request.headers}')
            filtered_headers = {key: value for key, value in response.headers.items() if key != 'Report-To'}
            cFormatter.print(Color.CYAN, f'Response Headers: {filtered_headers}')
            cFormatter.print(Color.CYAN, f'Response Body: {response.text}')
            cFormatter.print_separators(30, '-')
            return True
        except requests.RequestException as e:
            cFormatter.print(Color.CRITICAL, f'Login failed. {e}', isLogging=True)
            return False
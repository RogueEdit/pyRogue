# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 05.06.2024 

import os

from utilities.cFormatter import cFormatter, Color
import requests
from utilities.headers import user_agents, header_languages
import random
<<<<<<< HEAD
from colorama import init, Fore, Style
import brotli
=======
from colorama import init
<<<<<<< HEAD
>>>>>>> fc832e9 (giga refactoring nearing an end)
=======
from typing import List, Dict
>>>>>>> f8d0f9c (header fix)

init()

class HeaderGenerator:
    """
    A class to generate randomized but valid HTTP headers with User-Agent strings.
    The class maintains lists of different components used to construct User-Agent strings and headers.
    """

    file_path = './logs/headerfile-save'
    file_path_public = './logs/headerfile-public'
    git_url = 'https://raw.githubusercontent.com/RogueEdit/.github/main/headergen-data'

    if os.path.exists(file_path):

        with open(file_path, 'r') as f:
            headers = f.read()
    else:

        response = requests.get(git_url)

        if response.status_code == 200:
            headers_response = response.text

            with open(file_path_public, 'w') as f:
                headers = f.write(headers_response)
            
            with open(file_path, 'w') as f:
                headers = f.write(headers_response)
            
            with open(file_path, 'r') as f:
                headers = f.read()

    exec(headers)

    @classmethod
    def generate_user_agent(cls, os: str, browser: str) -> str:
        """
        Generate a User-Agent string based on the given operating system and browser.
        """
        return f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/88.0.4324.150 Safari/537.36"

    @classmethod
    def generate_headers(cls, auth_token: str = None) -> Dict[str, str]:
        """
        Generate randomized but valid HTTP headers including a User-Agent string.
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
        Logs in to the pokerogue.net API.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        data = {'username': self.username, 'password': self.password}
        try:
            headers = HeaderGenerator.generate_headers()
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
# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 06.06.2024 

import json
import requests
import os
import random
from colorama import init
from typing import List, Dict, Optional
from time import sleep

from utilities.limiter import Limiter
from utilities.cFormatter import cFormatter, Color
limiter = Limiter(lockout_period=30, timestamp_file='./data/extra.json')
init()

headerfile_save = './data/headerfile-save.json'

def handle_error_response(response: requests.Response) -> Dict[str, str]:
    """
    Handle error responses from the server.

    Args:
        response (requests.Response): The HTTP response object.

    Returns:
        dict: Empty dictionary.

    This method handles various HTTP response status codes and prints corresponding
    messages using the cFormatter class. It covers common client and server error
    codes, information from cloudflare docs.

    Example:
        >>> response = requests.get("https://example.com")
        >>> handle_error_response(response)
        'Response 404 - Not Found: The server can not find the requested resource.'
    """
    if response.status_code == 200:
        cFormatter.print(Color.BRIGHT_GREEN, 'Response 200 - That seemed to have worked!', isLogging=True)
        cFormatter.print(Color.BRIGHT_GREEN, 'If it doesn\'t apply in-game, refresh without cache or try a private tab!', isLogging=True)
    elif response.status_code == 400:
        cFormatter.print(Color.WARNING, 'Response 400 - Bad Request: The server could not understand the request due to invalid syntax. This is usually related to wrong credentials.', isLogging=True)
        cFormatter.print(Color.WARNING, 'Please retry a couple times. It this persists report on GitHub (can happen 3-5 times)')
    elif response.status_code == 401:
        cFormatter.print(Color.BRIGHT_RED, 'Response 401 - Unauthorized: Authentication is required and has failed or has not yet been provided.', isLogging=True)
    elif response.status_code == 403:
        cFormatter.print(Color.BRIGHT_RED, 'Response 403 - Forbidden. We have no authoriazion to acces the resource.', isLogging=True)
    elif response.status_code == 404:
        cFormatter.print(Color.BRIGHT_RED, 'Response 404 - Not Found: The server can not find the requested resource.', isLogging=True)
    elif response.status_code == 405:
        cFormatter.print(Color.BRIGHT_RED, 'Response 405 - Method Not Allowed: The request method is known by the server but is not supported by the target resource.', isLogging=True)
    elif response.status_code == 406:
        cFormatter.print(Color.BRIGHT_RED, 'Response 406 - Not Acceptable: The server cannot produce a response matching the list of acceptable values defined in the request\'s proactive content negotiation headers.', isLogging=True)
    elif response.status_code == 407:
        cFormatter.print(Color.BRIGHT_RED, 'Response 407 - Proxy Authentication Required: The client must first authenticate itself with the proxy.', isLogging=True)
    elif response.status_code == 408:
        cFormatter.print(Color.BRIGHT_RED, 'Response 408 - Request Timeout: The server would like to shut down this unused connection.', isLogging=True)
    elif response.status_code == 413:
        cFormatter.print(Color.BRIGHT_RED, 'Response 413 - Payload Too Large: The request entity is larger than limits defined by server.', isLogging=True)
    elif response.status_code == 429:
        cFormatter.print(Color.BRIGHT_RED, 'Response 429 - Too Many Requests: The user has sent too many requests in a given amount of time ("rate limiting").', isLogging=True)
    elif response.status_code == 500:
        cFormatter.print(Color.CRITICAL, 'Error 500 - Internal Server Error: The server has encountered a situation it does not know how to handle.', isLogging=True)
    elif response.status_code == 502:
        cFormatter.print(Color.CRITICAL, 'Error 502 - Bad Gateway: The server was acting as a gateway or proxy and received an invalid response from the upstream server.', isLogging=True)
    elif response.status_code == 503:
        cFormatter.print(Color.CRITICAL, 'Error 503 - Service Temporarily Unavailable: The server is not ready to handle the request.', isLogging=True)
    elif response.status_code == 504:
        cFormatter.print(Color.CRITICAL, 'Error 504 - Gateway Timeout: The server is acting as a gateway or proxy and did not receive a timely response from the upstream server.', isLogging=True)
    elif response.status_code == 520:
        cFormatter.print(Color.CRITICAL, 'Error 520 - Web Server Returns an Unknown Error: The server has returned an unknown error.', isLogging=True)
    elif response.status_code == 521:
        cFormatter.print(Color.CRITICAL, 'Error 521 - Web Server Is Down: The server is not responding to Cloudflare requests.', isLogging=True)
    elif response.status_code == 522:
        cFormatter.print(Color.CRITICAL, 'Error 522 - Connection Timed Out: Cloudflare was able to complete a TCP connection to the origin server, but the origin server did not reply with an HTTP response.', isLogging=True)
    elif response.status_code == 523:
        cFormatter.print(Color.CRITICAL, 'Error 523 - Origin Is Unreachable: Cloudflare could not reach the origin server.', isLogging=True)
    elif response.status_code == 524:
        cFormatter.print(Color.CRITICAL, 'Error 524 - A Timeout Occurred: Cloudflare was able to complete a TCP connection to the origin server, but the origin server did not reply with an HTTP response.', isLogging=True)
    else:
        cFormatter.print(Color.CRITICAL, 'Unexpected response received from the server.', isLogging=True)
    return {}

class HeaderGenerator:

    @classmethod
    def load_headers(cls) -> Dict[str, str]:
        """
        Load headers from the headerfile-save.json file and assign attributes.

        Returns:
            Dict[str, str]: Loaded headers.
        """
        if os.path.exists(headerfile_save):
            try:
                with open(headerfile_save, 'r') as f:
                    headers = json.load(f)
                    return headers
            except Exception as e:
                print(f'Failed to load headers. {e}')
        return {}

    @classmethod
    def save_headers(cls, headers: Dict[str, str]) -> None:
        """
        Save headers to headerfile-save.json.

        Args:
            headers (Dict[str, str]): Headers to save.
        """
        with open(headerfile_save, 'w') as f:
            json.dump(headers, f, indent=4)

    @classmethod
    def generate_headers(cls, isAuthHeader: bool = False) -> Dict[str, str]:
        chrome_major_versions = list(range(110, 126))
        sec_ch_ua_platform = ["Windows", "Macintosh", "X11"]
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 6.1; Win64; x64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Ubuntu; Linux x86_64",
        ]

        random_platform = random.choice(platforms)
        random_sec_ch_ua_platform = random.choice(sec_ch_ua_platform)
        random_chrome_major_version = random.choice(chrome_major_versions)

        headers = {
            "Accept": "application/x-www-form-urlencoded",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://pokerogue.net",
            "Referer": "https://pokerogue.net/",
            "Sec-Ch-Ua": f'"Google Chrome";v="{random_chrome_major_version}", "Chromium";v="{random_chrome_major_version}", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": f'"{random_sec_ch_ua_platform}"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": f"Mozilla/5.0 ({random_platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random_chrome_major_version}.0.0.0 Safari/537.36",
        }
        return headers
    
class loginLogic:
    LOGIN_URL = 'https://api.pokerogue.net/account/login'

    def __init__(self, username: str, password: str) -> None:
        """
        Initialize loginLogic with username and password.

        Args:
            username (str): The username for login.
            password (str): The password for login.

        Example:
            >>> login = loginLogic('user', 'pass')
        """
        self.username = username
        self.password = password
        self.token: Optional[str] = None
        self.session_id: Optional[str] = None
        self.session = requests.Session()

    @limiter.lockout
    def login(self) -> bool:
        """
        Perform login and handle responses.

        Returns:
            bool: True if login is successful, False otherwise.

        Example:
            >>> login = loginLogic('user', 'pass')
            >>> success = login.login()
            >>> print(success)
            True
        """
        data = {'username': self.username, 'password': self.password}
        try:
            headers = HeaderGenerator.generate_headers()
            # Faking 403
            # headers = {'Authorization': 'Bearer invalid_token'}
            cFormatter.print(Color.DEBUG, 'Adding delay to appear more natural to the server.')
            response = self.session.post(self.LOGIN_URL, headers=headers, data=data)
            sleep(3)
            response.raise_for_status()

            login_response = response.json()
            self.token = login_response.get('token')
            cFormatter.print_separators(30, '-')
            cFormatter.print(Color.GREEN, f'Login successful.')
            status_code_color = Color.BRIGHT_GREEN if response.status_code == 200 else Color.BRIGHT_RED
            cFormatter.print(status_code_color, f'HTTP Status Code: {response.status_code}', isLogging=True)
            cFormatter.print(Color.CYAN, f'Response URL: {response.request.url}', isLogging=True)
            # Filter and print response headers
            filtered_headers = {key: value for key, value in response.headers.items() if key != 'Report-To'}
            # Debug prints
            cFormatter.print(Color.CYAN, f'Response Headers: {filtered_headers}', isLogging=True)
            # cFormatter.print(Color.CYAN, f'Response Body: {response.text}', isLogging=True)
            cFormatter.print_separators(30, '-')
            return True

        except requests.RequestException as e:
            handle_error_response(response)
            return False
# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 05.06.2024 

import json
import requests
import os
import random
from colorama import init
from typing import List, Dict

from utilities.limiter import Limiter
from utilities.cFormatter import cFormatter, Color
limiter = Limiter(lockout_period=10, timestamp_file='./data/extra.json')
init()

def handle_error_response(response: requests.Response) -> dict:
    """
    Handle error responses from the server.

    Args:
        response (requests.Response): The HTTP response object.

    Returns:
        dict: Empty dictionary.

    This method handles various HTTP response status codes and prints corresponding
    messages using the cFormatter class. It covers common client and server error
    codes, information from cloudflare docs.
    """
    if response.status_code == 200:
        cFormatter.print(Color.BRIGHT_GREEN, 'Response 200 - That seemed to have worked!', isLogging=True)
        cFormatter.print(Color.BRIGHT_GREEN, 'If it doesn\'t apply in-game, refresh without cache or try a private tab!', isLogging=True)
    elif response.status_code == 400:
        cFormatter.print(Color.WARNING, 'Response 400 - Bad Request: The server could not understand the request due to invalid syntax. This is usually related to wrong credentials.', isLogging=True)
    elif response.status_code == 401:
        cFormatter.print(Color.BRIGHT_RED, 'Response 401 - Unauthorized: Authentication is required and has failed or has not yet been provided.', isLogging=True)
    elif response.status_code == 403:
        HeaderGenerator.handle_dynamic_header_data()
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

class HeaderGenerator:
    retry_count = 0
    headerfile = './data/headerfile-save.json'
    headerfile_public = './data/headerfile-public.json'
    git_url = 'https://raw.githubusercontent.com/RogueEdit/onlineRogueEditor/headerfile/headerfile-public.json'
    extra_file_path = './data/extra.json'

    @classmethod
    def load_headers(cls) -> Dict[str, str]:
        if os.path.exists(cls.headerfile_public):
            with open(cls.headerfile_public, 'r') as f:
                headers = json.load(f)
                cls.set_attributes(headers)
                return cls.generate_headers()
        else:
            response = requests.get(cls.git_url)
            if response.status_code == 200:
                headers_response = response.json()
                with open(cls.headerfile_public, 'w') as f:
                    json.dump(headers_response, f, indent=4)
                cls.set_attributes(headers_response)
                return cls.generate_headers()
        return {}

    @classmethod
    def set_attributes(cls, headers: Dict[str, list]) -> None:
        cls.operating_systems = headers.get('operating_systems', {})
        cls.browsers = headers.get('browsers', [])
        cls.static_headers = headers.get('static_headers', {})
        cls.platforms = headers.get('platforms', {})

    @classmethod
    def save_headers(cls, headers: Dict[str, str]) -> None:
        with open(cls.headerfile, 'w') as f:
            json.dump(headers, f, indent=4)

    @classmethod
    def generate_user_agent(cls, os: str, browser: str) -> str:
        return f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/88.0.4324.150 Safari/537.36"

    @classmethod
    def generate_headers(cls, auth_token: str = None) -> Dict[str, str]:
        if not hasattr(cls, 'operating_systems'):
            cls.load_headers()

        device = random.choice(list(cls.operating_systems.keys()))
        os = random.choice(cls.operating_systems[device])
        browser = random.choice(cls.browsers)
        user_agent = cls.generate_user_agent(os, browser)

        headers = cls.static_headers.copy()
        headers.update({
            'User-Agent': user_agent,
            'Sec-Ch-Ua-Platform': cls.platforms.get(device, ''),
        })

        if auth_token:
            headers['Authorization'] = auth_token

        return headers

    @classmethod
    def read_403_count(cls) -> int:
        if not os.path.exists(cls.extra_file_path):
            return 0
        try:
            with open(cls.extra_file_path, 'r') as f:
                data = json.load(f)
                return data.get('total_403_errors', 0)
        except json.JSONDecodeError as e:
            return 0

    @classmethod
    def write_403_count(cls, count: int) -> None:
        data = {}
        if os.path.exists(cls.extra_file_path):
            try:
                with open(cls.extra_file_path, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f'DEBUG: JSONDecodeError while reading extra file: {e}')
        
        data['total_403_errors'] = count
        
        with open(cls.extra_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def handle_dynamic_header_data(cls, force_fetch: bool = False) -> None:
        total_403_errors = cls.read_403_count()

        if force_fetch or total_403_errors >= 3:
            cls.retry_count = 3  # Set retry_count to 3 to force fetch

        cls.retry_count += 1

        # Always delete the existing header file
        if os.path.exists(cls.headerfile):
            os.remove(cls.headerfile)

        if cls.retry_count < 3:
            cFormatter.print(Color.CRITICAL, 'Response 403 - Forbidden: The client does not have access rights to the content.', isLogging=True)
            cFormatter.print(Color.INFO, 'Headers refetched restart the tool.', isLogging=True)
            cFormatter.print(Color.BRIGHT_CYAN, f'Total number of 403 errors encountered: {total_403_errors}', isLogging=True)
            headers = cls.generate_headers()
            cls.save_headers(headers)
            # Write the current 403 count to extra.json
            total_403_errors += 1  # Increment the total 403 error count
            cls.write_403_count(total_403_errors)
        else:
            response = requests.get(cls.git_url)
            if response.status_code == 200:
                try:
                    headers_response = response.json()
                    cls.set_attributes(headers_response)
                    headers = cls.generate_headers()
                    cls.save_headers(headers)
                    cls.retry_count = 0  # Reset the counter
                    # Reset total_403_errors count in the JSON file after fetch
                    cls.write_403_count(0)
                except json.JSONDecodeError as e:
                    print(f'DEBUG: JSONDecodeError while decoding response content: {e}')
            else:
                print(f'DEBUG: Failed to fetch headers from remote source, status_code={response.status_code}')

        if force_fetch:
            cFormatter.print(Color.BRIGHT_GREEN, 'Header data new constructed. Restart the tool.', isLogging=True)
            cFormatter.print(Color.BRIGHT_CYAN, f'Total number of 403 errors encountered reset.', isLogging=True)


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

    @limiter.lockout
    def login(self) -> bool:
        data = {'username': self.username, 'password': self.password}
        try:
            # Load headers, utilizing the saved header file if it exists
            headers = HeaderGenerator.load_headers()
            
            #faking 403
            #headers = {'Authorization': 'Bearer invalid_token'}

            if not headers:
                headers = HeaderGenerator.generate_headers()
            # Make the POST request with the generated headers
            response = self.session.post(self.LOGIN_URL, headers=headers, data=data)
            cFormatter.print(Color.CYAN, f'Response URL: {response.request.url}', isLogging=True)
            cFormatter.print(Color.CYAN, f'Response Headers: {response.request.headers}', isLogging=True)
            response.raise_for_status()

            # Process the response
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

            # Filter and print response headers
            filtered_headers = {key: value for key, value in response.headers.items() if key != 'Report-To'}
            cFormatter.print(Color.CYAN, f'Response Headers: {filtered_headers}', isLogging=True)
            cFormatter.print(Color.CYAN, f'Response Body: {response.text}', isLogging=True)
            cFormatter.print_separators(30, '-')
            
            return True

        except requests.RequestException as e:
            handle_error_response(response)
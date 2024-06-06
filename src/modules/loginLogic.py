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
    return {}

class HeaderGenerator:
    retry_count = 0
    headerfile_save = './data/headerfile-save.json'
    headerfile_public = './data/headerfile-public.json'
    extra_file_path = './data/extra.json'
    git_url = 'https://raw.githubusercontent.com/RogueEdit/onlineRogueEditor/headerfile/headerfile-public.json'
    user_agents: List[str] = []
    static_headers: Dict[str, str] = []

    @classmethod
    def set_attributes(cls, headers: Dict[str, List[str]]) -> None:
        """
        Set user agents and static headers.

        Args:
            headers (Dict[str, List[str]]): Dictionary containing user agents and static headers.

        Example:
            >>> HeaderGenerator.set_attributes({'user_agents': ['Mozilla/5.0'], 'static_headers': {'Content-Type': 'application/json'}})
        """
        cls.user_agents = headers.get('user_agents', [])
        cls.static_headers = headers.get('static_headers', {})

    @classmethod
    def load_user_agents(cls) -> None:
        """
        Load user agents from headerfile-public.json and assign them to user_agents attribute.

        Example:
            >>> HeaderGenerator.load_user_agents()
        """
        try:
            with open(cls.headerfile_public, 'r') as f:
                data = json.load(f)
                cls.user_agents = data.get('user_agents', [])
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Failed to load user agents. {e}', isLogging=True)

    @classmethod
    def load_headers(cls) -> Dict[str, str]:
        """
        Load headers from the headerfile-save.json file and assign attributes.

        Returns:
            Dict[str, str]: Loaded headers.

        Example:
            >>> headers = HeaderGenerator.load_headers()
            >>> print(headers)
            {'User-Agent': 'Mozilla/5.0'}
        """
        if os.path.exists(cls.headerfile_save):
            try:
                with open(cls.headerfile_save, 'r') as f:
                    headers = json.load(f)
                    cls.set_attributes(headers)
                    # cFormatter.print(Color.DEBUG, f'Headers loaded from {cls.headerfile_save}: {headers}')
                    return headers
            except Exception as e:
                cFormatter.print(Color.DEBUG, f'Something unexpected happened. Headers reloaded from {cls.headerfile_save}: {e}')
        return {}

    @classmethod
    def save_headers(cls, headers: Dict[str, str]) -> None:
        """
        Save headers to headerfile-save.json.

        Args:
            headers (Dict[str, str]): Headers to save.

        Example:
            >>> HeaderGenerator.save_headers({'User-Agent': 'Mozilla/5.0'})
        """
        with open(cls.headerfile_save, 'w') as f:
            json.dump(headers, f, indent=4)

    @classmethod
    def generate_headers(cls, auth_token: Optional[str] = None, onlySetup: bool = False) -> Dict[str, str]:
        """
        Generate headers for HTTP requests.

        Args:
            auth_token (str, optional): Authorization token. Defaults to None.
            onlySetup (bool, optional): Whether to only set up headers without saving them. Defaults to False.

        Returns:
            Dict[str, str]: Generated headers.

        Example:
            >>> headers = HeaderGenerator.generate_headers()
            >>> print(headers)
            {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        """
        headers: Dict[str, str] = {}

        # Check if headerfile-public.json exists and fetch if not
        if not os.path.exists(cls.headerfile_public):
            cFormatter.print(Color.WARNING, f'{cls.headerfile_public} not found. Fetching from {cls.git_url}.', isLogging=True)
            response = requests.get(cls.git_url)
            if response.status_code == 200:
                with open(cls.headerfile_public, 'w') as f:
                    f.write(response.text)
                cFormatter.print(Color.BRIGHT_GREEN, f'Successfully fetched {cls.headerfile_public} from {cls.git_url}.', isLogging=True)
            else:
                cFormatter.print(Color.CRITICAL, f'Failed to fetch {cls.headerfile_public} from {cls.git_url}.', isLogging=True)

        try:
            with open(cls.headerfile_public, 'r') as f:
                data = json.load(f)
                user_agents = data.get('user_agents', [])
                static_headers = data.get('static_headers', {})  # Retrieve static headers from the JSON file
                if not user_agents:
                    cFormatter.print(Color.INFO, 'No user agents found in headerfile-public.json')

                # Use user_agents from file
                user_agent = random.choice(user_agents)
                headers.update(static_headers)  # Update headers with static headers
                headers.update({'User-Agent': user_agent})  # Add the random user agent to headers

                if not onlySetup:
                    cls.save_headers(headers)

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Failed to generate headers. {e}', isLogging=True)

        return headers

    @classmethod
    def read_403_count(cls) -> int:
        """
        Read the count of 403 errors from the extra.json file.

        Returns:
            int: Count of 403 errors.

        Example:
            >>> count = HeaderGenerator.read_403_count()
            >>> print(count)
            2
        """
        if not os.path.exists(cls.extra_file_path):
            return 0
        try:
            with open(cls.extra_file_path, 'r') as f:
                data = json.load(f)
                return data.get('total_403_errors', 0)
        except json.JSONDecodeError as e:
            cFormatter.print(Color.CRITICAL, f'JSONDecodeError while reading extra.json {e}', isLogging=True)
            return 0

    @classmethod
    def write_403_count(cls, count: int) -> None:
        """
        Write the count of 403 errors to the extra.json file.

        Args:
            count (int): Count of 403 errors.

        Example:
            >>> HeaderGenerator.write_403_count(3)
        """
        data = {}
        if os.path.exists(cls.extra_file_path):
            try:
                with open(cls.extra_file_path, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                data = {}

        data['total_403_errors'] = count

        with open(cls.extra_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def handle_dynamic_header_data(cls, force_fetch: bool = False) -> None:
        """
        Handle dynamic header data when a 403 error occurs too frequently.

        Args:
            force_fetch (bool, optional): Whether to force fetch header data. Defaults to False.

        Example:
            >>> HeaderGenerator.handle_dynamic_header_data()
        """
        total_403_errors = cls.read_403_count()

        if force_fetch or total_403_errors >= 3:
            retry_count = 3  # Set retry_count to 3 to force fetch
        else:
            retry_count = getattr(cls, 'retry_count', 0) + 1  # Increment retry_count if it exists

        # Always delete the existing header file
        if os.path.exists(cls.headerfile_save):
            os.remove(cls.headerfile_save)

        if retry_count < 3:
            # Write the current 403 count to extra.json
            total_403_errors += 1  # Increment the total 403 error count
            cls.write_403_count(total_403_errors)
            cFormatter.print(Color.CRITICAL, 'Response 403 - Forbidden: The client does not have access rights to the content.', isLogging=True)
            cFormatter.print(Color.CRITICAL, f'Total number of 403 errors encountered: {total_403_errors}', isLogging=True)
            cFormatter.print(Color.CRITICAL, f'Please retry {3 - total_403_errors} more times. Then we will try to rebuild header data...', isLogging=True)
        else:
            cFormatter.print(Color.CRITICAL, 'Response 403 - Forbidden: The client does not have access rights to the content.', isLogging=True)
            cFormatter.print(Color.CRITICAL, 'We encountered this too often, refetching seeds. Please restart the tool when succesful.', isLogging=True)
            # Perform fetch from remote source
            response = requests.get(cls.git_url)
            if response.status_code == 200:
                cFormatter.print(Color.BRIGHT_GREEN, 'Success! We were able to fetch new header seeds. Please restart.', isLogging=True)
                try:
                    headers_response = response.json()
                    cls.set_attributes(headers_response)
                    cls.retry_count = 0  # Reset the counter
                    # Reset total_403_errors count in the JSON file after fetch
                    cls.write_403_count(0)
                    cFormatter.print(Color.BRIGHT_GREEN, 'Hope the best this headers work to login!', isLogging=True)
                except json.JSONDecodeError as e:
                    cFormatter.print(Color.BRIGHT_GREEN, f'JSON Decode Error {e}', isLogging=True)
            else:
                cFormatter.print(Color.RED, 'Failed to fetch headers from source', isLogging=True)

        if force_fetch:
            cFormatter.print(Color.BRIGHT_GREEN, 'Header data newly constructed. Restart the tool.', isLogging=True)
            cFormatter.print(Color.BRIGHT_CYAN, f'Total number of 403 errors encountered reset.', isLogging=True)


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
            if self.token:
                cFormatter.print(Color.CYAN, f'Token: {self.token}')
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
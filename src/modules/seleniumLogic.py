# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 06.06.2024 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modules.mainLogic import Rogue
import json
import time
import requests
from typing import Optional, Tuple, Dict, Any

class SeleniumLogic:
    """
    Handles the Selenium-based login process for PokeRogue.

    Attributes:
        username (str): The username for login.
        password (str): The password for login.
        timeout (int): The timeout duration for the login process.
        session (requests.Session): The requests session for handling HTTP requests.
        selenium_headers (Dict): Headers used in the Selenium session.
    """

    def __init__(self, username: str, password: str, timeout: int) -> None:
        """
        Initializes the SeleniumLogic instance.

        Args:
            username (str): The username for login.
            password (str): The password for login.
            timeout (int): The timeout duration for the login process.
        """
        self.timeout = timeout
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.selenium_headers = {}

    def _process_browser_log_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a single browser log entry to extract the relevant response data.

        Args:
            entry (Dict[str, Any]): A log entry from the browser.

        Returns:
            Dict[str, Any]: The processed response data.
        """
        response = json.loads(entry['message'])['message']
        return response

    def print_until_timeout(self) -> None:
        """
        Prints a message repeatedly until the timeout duration is reached.
        """
        timeout_seconds = self.timeout
        start_time = time.time()

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= timeout_seconds:
                break

            print("Please do not log in manually now in the newly opened browser. Wait until the browser closes and do not touch anything.")
            time.sleep(1)

    def logic(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Handles the login logic using Selenium and retrieves the session ID and token.

        Returns:
            Tuple[Optional[str], Optional[str]]: The session ID and token if available, otherwise None.
        """
        opts = webdriver.ChromeOptions()
        opts.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        opts.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=opts)
        url = "https://www.pokerogue.net/"
        driver.get(url)

        self.print_until_timeout()

        # Locate and fill the username and password fields
        username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(10)  # Wait for the login to complete

        # Retrieve the browser log
        browser_log = driver.get_log('performance')
        events = [self._process_browser_log_entry(entry) for entry in browser_log]

        session_id = None
        for event in events:
            if 'response' in event['params']:
                response = event["params"]["response"]
                if 'url' in response:
                    url = response['url']
                    if 'clientSessionId' in url:
                        session_id = url.split('clientSessionId=')[1]
                        break

        token = None
        for event in events:
            if 'method' in event and event['method'] == 'Network.responseReceived':
                response = event['params']['response']
                if response['url'] == 'https://api.pokerogue.net/account/login':
                    request_id = event['params']['requestId']
                    result = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    response_body = result.get('body', '')
                    if response_body:
                        token_data = json.loads(response_body)
                        token = token_data.get('token')
                        if token:
                            break

        print("Session ID:", session_id)
        print("Token:", token)

        driver.quit()

        return session_id, token
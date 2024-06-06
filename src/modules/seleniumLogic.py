# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 06.06.2024 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time
from typing import Optional, Tuple, Dict, Any
from modules.loginLogic import HeaderGenerator
from utilities.logger import CustomLogger

class SeleniumLogic:
    """
    Handles the Selenium-based login process for PokeRogue.

    Attributes:
        username (str): The username for login.
        password (str): The password for login.
        timeout (int): The timeout duration for the login process.
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

    def logic(self) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
        """
        Handles the login logic using Selenium and retrieves the session ID, token, and headers.

        Returns:
            Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]: The session ID, token, and headers if available, otherwise None.
        """
        CustomLogger.deactivate_logging()
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        driver = webdriver.Chrome(options=options)
        url = "https://www.pokerogue.net/"
        driver.get(url)

        try:
            # Wait for the username field to be visible and input the username
            username_field = WebDriverWait(driver, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )
            username_field.send_keys(self.username)

            # Wait for the password field to be visible and input the password
            password_field = WebDriverWait(driver, self.timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
            )
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

            print("Waiting for login data...")
            start_time = time.time()
            while True:
                time.sleep(1)
                browser_log = driver.get_log('performance')
                events = [self._process_browser_log_entry(entry) for entry in browser_log]

                session_id = None
                token = None
                headers = None

                for event in events:
                    if 'response' in event['params']:
                        response = event["params"]["response"]
                        if 'url' in response:
                            url = response['url']
                            if 'clientSessionId' in url:
                                session_id = url.split('clientSessionId=')[1]
                    if 'method' in event and event['method'] == 'Network.requestWillBeSent':
                        request = event['params']['request']
                        if request['url'] == 'https://api.pokerogue.net/account/login':
                            headers = request['headers']
                    if 'method' in event and event['method'] == 'Network.responseReceived':
                        response = event['params']['response']
                        if response['url'] == 'https://api.pokerogue.net/account/login':
                            request_id = event['params']['requestId']
                            result = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                            response_body = result.get('body', '')
                            if response_body:
                                token_data = json.loads(response_body)
                                token = token_data.get('token')

                if session_id and token and headers:
                    break

                print("Still waiting for login data...")

                elapsed_time = time.time() - start_time
                if elapsed_time >= self.timeout:
                    print("Timeout occurred.")
                    break

        except TimeoutException as e:
            print(f"Timeout occurred: {e}")

        finally:
            HeaderGenerator.save_headers(headers=headers)
            driver.quit()

        CustomLogger.reactivate_logging()
        print("Session ID:", session_id)
        print("Token:", token)
        print("Request Headers:", json.dumps(headers, indent=2))


        return session_id, token, headers

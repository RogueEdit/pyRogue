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
from utilities.logger import CustomLogger
import random

"""
Usage Example:
    # Initialize SeleniumLogic with username, password, and optional timeout
    >>> selenium_logic = SeleniumLogic(username="your_username", password="your_password", timeout=120)

    # Execute the login logic
    >>> session_id, token, headers = selenium_logic.logic()

    # Output the results
    >> print(f"Session ID: {session_id}")
    >> print(f"Token: {token}")
    >> print(f"Headers: {headers}")

Expected Output Example:
    >> Session ID: abc123clientSessionId
    >> Token: abc123token
    >> Headers: {'Content-Type': 'application/json', 'User-Agent': '...'}
"""

class SeleniumLogic:
    """
    Handles the Selenium-based login process for pyRogue.

    Attributes:
    >> username (str): The username for login.
    >> password (str): The password for login.
    >> timeout (int): The timeout duration for the login process.
    """

    def __init__(self, username: str, password: str, timeout: int = 120, useScripts = None) -> None:
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
        self.useScripts = useScripts

    def _process_browser_log_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a single browser log entry to extract the relevant response data.

        Args:
        >> entry (Dict[str, Any]): A log entry from the browser.

        Returns:
        >> Dict[str, Any]: The processed response data.
        """
        response = json.loads(entry['message'])['message']
        return response

    def logic(self) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
        """
        Handles the login logic using Selenium and retrieves the session ID, token, and headers.

        Returns:
        >> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]: The session ID, token, and headers if available, otherwise None.
        """
        # Deactivate logging because selenium clutters it extremely
        CustomLogger.deactivate_logging()

        # Set Browser options
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'}) # All performance logs
        options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
        options.add_argument("--no-sandbox")  # Overcome limited resource problems
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        options.add_argument("--disable-infobars")  # Disable infobars
        options.add_argument("--enable-javascript") # enable javascript explicitly

        driver = webdriver.Chrome(options=options)
        url = "https://www.pokerogue.net/"
        driver.get(url)

        session_id = None
        token = None

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

            # Send RETURN key
            password_field.send_keys(Keys.RETURN)

            print('Waiting for login data...')
            time.sleep(random.randint(8,12))  # Fixed wait time to ensure data is there

            # Process the browser log
            browser_log = driver.get_log('performance')
            events = [self._process_browser_log_entry(entry) for entry in browser_log]

            # Extract session data such as sessionId, auth-token or headers etc
            for event in events:
                # Extract the clientSessionId
                if 'response' in event['params']:
                    response = event["params"]["response"]
                    if 'url' in response:
                        url = response['url']
                        if 'clientSessionId' in url:
                            session_id = url.split('clientSessionId=')[1]
                # Extract the authorization token
                if 'method' in event and event['method'] == 'Network.responseReceived':
                    response = event['params']['response']
                    if response['url'] == 'https://api.pokerogue.net/account/login':
                        request_id = event['params']['requestId']
                        result = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                        response_body = result.get('body', '')
                        if response_body:
                            token_data = json.loads(response_body)
                            token = token_data.get('token')

        # When we go over a specified time
        except TimeoutException as e:
            print(f"Timeout occurred: {e}")

        # When our try is done we finalize with closing the browser, reactivating logging
        finally:
            CustomLogger.reactivate_logging()
            # If we are not using login method 3 we should close the driver already
            if not self.useScripts:
                driver.close()
           
        return session_id, token, driver

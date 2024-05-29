from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modules.rogueApiClass import RogueAPI
import json
import time

class SeleniumLogic:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
    
    def _process_browser_log_entry(self, entry):
        response = json.loads(entry['message'])['message']
        return response
    
    def print_until_timeout(self):
        timeout_seconds = 60
        start_time = time.time()
        
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            if elapsed_time >= timeout_seconds:
                break
            
            print("Please do not log-in manually now in the new opened browser. Wait until the browser closes and do not touch anything.")
            time.sleep(1)  

    def logic(self):
        opts = webdriver.ChromeOptions()
        opts.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        opts.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=opts)

        # URL of the website to be accessed
        url = "https://www.pokerogue.net/"

        # Open the specified URL in the browser
        driver.get(url)

        # Wait for 20 seconds to allow the page to load completely
        self.print_until_timeout()

        username_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")

        # Input the username and password into the respective fields
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)

        # Simulate pressing the 'Return' key to submit the login form
        password_field.send_keys(Keys.RETURN)

        # Wait for 10 seconds to allow the login process to complete
        time.sleep(10)

        # Retrieve the performance logs from the browser
        browser_log = driver.get_log('performance')

        # Process the log entries to extract response messages
        events = [self._process_browser_log_entry(entry) for entry in browser_log]

        # Extract clientSessionId if available
        responses = []
        session_id = None
        for event in events:
            
            if 'response' in event['params']:
                response = event["params"]["response"]

                if response:
                    responses.append(response)
                
                if 'url' in event['params']['response']:
                    url = event['params']['response']['url']
                
                if 'clientSessionId' in url:
                    session_id = url.split('clientSessionId=')[1]
                    break

        # Extract the token from the response body of the Network.responseReceived event
        token = None
        for event in events:
            if 'method' in event and event['method'] == 'Network.responseReceived':
                response = event['params']['response']
                if response['url'] == 'https://api.pokerogue.net/account/login':  # Check if it's the login response
                    request_id = event['params']['requestId']
                    # Get the response body using the request ID
                    result = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    response_body = result.get('body', '')
                    if response_body:
                        token_data = json.loads(response_body)
                        token = token_data.get('token')
                        if token:
                            break

        print("Session ID:", session_id)
        print("Token:", token)

        return RogueAPI(token, session_id)

        # time.sleep(69696969)

        # driver.quit()
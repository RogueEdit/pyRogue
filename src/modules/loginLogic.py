# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 04.06.2024 



import requests
from utilities.headers import user_agents
import random
from colorama import init, Fore, Style
import brotli

class loginLogic:
    LOGIN_URL = "https://api.pokerogue.net/account/login"
    HEADERS = {
        "Accept": "application/x-www-form-urlencoded",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://pokerogue.net/",
        "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    }

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.token = None
        self.session_id = None
        self.session = requests.Session()

    # we need the hide we are python already
    def _generate_headers(self) -> dict:
        random_user_agent = random.choice(user_agents)
        headers = {
            "Accept": "application/x-www-form-urlencoded",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://pokerogue.net/",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Platform": "Windows",
            "User-Agent": random_user_agent,
        }
        return headers

    def login(self) -> bool:
        data = {"username": self.username, "password": self.password}
        try:
            response = self.session.post(self.LOGIN_URL, headers=self.HEADERS, data=data)
            response.raise_for_status()
            login_response = response.json()
            self.token = login_response.get("token")

            print("--------------------------")
            print(Fore.GREEN + "Logged in successfully.")
            print("General Session data, you can ignore that - its when you have problems!" + Style.RESET_ALL)
            if self.token:
                print(f"Token: {self.token}")
            print(Style.RESET_ALL + f"HTTP Status Code: {Fore.RED if response.status_code >= 400 else Fore.GREEN}{response.status_code}{Style.RESET_ALL}")
            print(f"Request URL: {response.request.url}")
            print(f"Request Headers: {response.request.headers}")
            filtered_headers = {key: value for key, value in response.headers.items() if key != 'Report-To'}
            print(f"Response Headers: {filtered_headers}")
            print(f"Response Body: {response.text}")
            print(Fore.GREEN + "Looks good!" + Style.RESET_ALL)
            print("---------------------------")
            return True
        except requests.RequestException as e:
            print("--------------------------")
            print(Fore.RED + f"Login failed with requests: {e}" + Style.RESET_ALL)
            return False

    def get_auth_headers(self) -> dict:
        return {"authorization": self.token}
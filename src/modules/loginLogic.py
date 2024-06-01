import requests
import logging

logger = logging.getLogger(__name__)

class loginLogic:
    LOGIN_URL = "https://api.pokerogue.net/account/login"

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.token = None
        self.auth_headers = None
        self.session = requests.Session()

    def login(self) -> bool:
        data = {"username": self.username, "password": self.password}
        headers = {
            "Accept": "application/x-www-form-urlencoded",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://pokerogue.net/",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }
        try:
            print("Attempting login...")
            response = self.session.post(self.LOGIN_URL, json=data, headers=headers)
            print("Login request sent.")
            response.raise_for_status()
            print("Received response from server.")
            self.token = response.json().get("token")
            print("Token received:", self.token)
            self.auth_headers = {
                "authorization": self.token,
                "Accept": "application/x-www-form-urlencoded",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://pokerogue.net/",
                "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            }
            logger.info("Logged in successfully.")
            print("Logged in successfully.")
            print(f"Token: {self.token}")
            return True
        except requests.RequestException as e:
            logger.error("Login failed with requests: %s", e)
            print("Login failed with requests:", e)
            return False

    def get_auth_headers(self) -> dict:
        return self.auth_headers

import requests
import logging

logger = logging.getLogger(__name__)

class loginLogic:
    LOGIN_URL = "https://api.pokerogue.net/account/login"
    HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.auth_headers = None  # Initialize auth_headers attribute
        self.session = requests.Session()

    def login_with_requests(self) -> bool:
        data = {"username": self.username, "password": self.password}
        try:
            response = self.session.post(self.LOGIN_URL, json=data, headers=self.HEADERS)
            response.raise_for_status()
            token = response.json().get("token")
            self.auth_headers = {  # Set the auth_headers attribute
                "Authorization": f"Bearer {token}",
                "Accept": "application/x-www-form-urlencoded",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://pokerogue.net/",
                "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Windows",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            }
            logger.info("Logged in successfully with requests.")
            return True
        except requests.RequestException as e:
            logger.error("Login failed with requests: %s", e)
            return False

    def login(self) -> bool:
        return self.login_with_requests()

# loginLogic.py
import logging
import requests

logger = logging.getLogger(__name__)

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

    def __init__(self, session, username: str, password: str) -> None:
        self.session = session
        self.username = username
        self.password = password
        self.token = None
        self.session_id = None

    def login(self) -> bool:
        data = {"username": self.username, "password": self.password}
        try:
            response = self.session.post(self.LOGIN_URL, headers=self.HEADERS, data=data)
            response.raise_for_status()
            login_response = response.json()
            self.token = login_response.get("token")
            self.session_id = login_response.get("sessionID")
            logger.info("Logged in successfully.")
            print("Logged in successfully.")
            if self.token:
                print(f"Token: {self.token}")
            if self.session_id:
                print(f"Session ID: {self.session_id}")
            print(f"Username: {self.username}")
            return True
        except requests.RequestException as e:
            logger.error("Login failed with requests: %s", e)
            print("Login failed with requests:", e)
            return False

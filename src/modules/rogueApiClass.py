# rogueApiClass.py
from modules.rogueClass import Rogue

class RogueAPI:
    def __init__(self, auth_token: str, session_id: str) -> None:
        self.auth_token = auth_token
        self.session_id = session_id

    def login(self) -> Rogue:
        return Rogue(self.auth_token, self.session_id)
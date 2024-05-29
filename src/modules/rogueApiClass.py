from modules.rogueClass import Rogue

class RogueAPI:

    def __init__(self, auth_token, clientSessionId):
        self.auth_token = auth_token
        self.clientSessionId = clientSessionId

    def login(self):
        return Rogue(self.auth_token, self.clientSessionId)
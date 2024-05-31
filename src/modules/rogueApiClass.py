"""Module for interacting with the Rogue API."""

from modules.rogueClass import Rogue

class RogueAPI:
    """Class for interacting with the Rogue API."""

    def __init__(self, auth_token: str, clientSessionId: str) -> None:
        """
        Initialize RogueAPI object.

        Parameters:
        auth_token (str): The authentication token.
        clientSessionId (str): The client session ID.
        """
        self.auth_token = auth_token
        self.clientSessionId = clientSessionId

    def login(self) -> Rogue:
        """
        Log in using the authentication token and client session ID.

        Returns:
        Rogue: An instance of Rogue.
        """
        return Rogue(self.auth_token, self.clientSessionId)
# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 05.06.2024 

import unittest
from loginLogic import loginLogic

class TestLoginLogic(unittest.TestCase):
    """
    A test suite for the loginLogic class.
    """

    def test_login_success(self):
        """
        Test login method when login is successful.
        """
        username = "test_user"
        password = "test_password"
        logic = loginLogic(username, password)
        result = logic.login()
        self.assertTrue(result)

    def test_login_failure(self):
        """
        Test login method when login fails.
        """
        username = "invalid_user"
        password = "invalid_password"
        logic = loginLogic(username, password)
        result = logic.login()
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
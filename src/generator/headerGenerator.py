
import random
from typing import List, Dict

class HeaderGenerator:
    """
    A class to generate randomized but valid HTTP headers with User-Agent strings.
    The class maintains lists of different components used to construct User-Agent strings and headers.
    
    Attributes
    ----------
    browsers : List[str]
        A list of web browsers.
    operating_systems : Dict[str, List[str]]
        A dictionary mapping device types to lists of operating systems.
    devices : List[str]
        A list of device types.
    static_headers : Dict[str, str]
        A dictionary of static HTTP headers.
    """
    
    browsers: List[str] = [
        'Chrome', 'Firefox', 'Safari', 'Edge', 'Opera', 'Internet Explorer'
    ]
    
    operating_systems: Dict[str, List[str]] = {
        'Windows': ['Windows NT 10.0', 'Windows NT 6.1'],
        'Macintosh': ['Macintosh; Intel Mac OS X 10_15_7'],
        'X11': ['X11; Linux x86_64'],
        'Linux': ['X11; Linux x86_64'],
        'Android': ['Android 10', 'Android 9'],
        'iPhone': ['iPhone; CPU iPhone OS 14_0 like Mac OS X', 'iPhone; CPU iPhone OS 13_0 like Mac OS X']
    }
    
    devices: List[str] = list(operating_systems.keys())
    
    static_headers: Dict[str, str] = {
        "Accept": "application/json",
        "Accept-Language": "it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://pokerogue.net/",
        "Content-Type": "application/json",
        "content-encoding": "br",
        "Origin": "https://pokerogue.net/",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=1",
    }
    
    @classmethod
    def generate_user_agent(cls, device: str, os: str, browser: str) -> str:
        """
        Generate a User-Agent string based on given device, operating system, and browser.

        Parameters
        ----------
        device : str
            The type of device.
        os : str
            The operating system.
        browser : str
            The web browser.

        Returns
        -------
        str
            A User-Agent string constructed from the given parameters.
        """
        return f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/88.0.4324.150 Safari/537.36"

    @classmethod
    def generate_headers(cls, auth_token: str) -> Dict[str, str]:
        """
        Generate randomized but valid HTTP headers including a User-Agent string.

        Parameters
        ----------
        auth_token : str
            The authorization token to be included in the headers.

        Returns
        -------
        Dict[str, str]
            A dictionary containing HTTP headers.
        """
        device: str = random.choice(cls.devices)
        os: str = random.choice(cls.operating_systems[device])
        browser: str = random.choice(cls.browsers)
        user_agent: str = cls.generate_user_agent(device, os, browser)
        
        headers: Dict[str, str] = cls.static_headers.copy()
        headers.update({
            "authorization": auth_token,
            "User-Agent": user_agent,
        })
        
        return headers

    @classmethod
    def get_browsers(cls) -> List[str]:
        """
        Get the list of browsers.

        Returns
        -------
        List[str]
            A list of browser names.
        """
        return cls.browsers

    @classmethod
    def get_operating_systems(cls) -> Dict[str, List[str]]:
        """
        Get the dictionary of operating systems.

        Returns
        -------
        Dict[str, List[str]]
            A dictionary of device types to operating system lists.
        """
        return cls.operating_systems

    @classmethod
    def get_devices(cls) -> List[str]:
        """
        Get the list of devices.

        Returns
        -------
        List[str]
            A list of device types.
        """
        return cls.devices


if __name__ == "__main__":
    # Generate fake HTTP headers with an authorization token
    auth_token = "your_auth_token_here"
    headers = HeaderGenerator.generate_headers(auth_token)
    print(headers)

    # Get the list of browsers
    browsers = HeaderGenerator.get_browsers()
    print(browsers)

    # Get the dictionary of operating systems
    operating_systems = HeaderGenerator.get_operating_systems()
    print(operating_systems)

    # Get the list of devices
    devices = HeaderGenerator.get_devices()
    print(devices)

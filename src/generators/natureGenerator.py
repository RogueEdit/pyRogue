# Authors: RogueEdit Organization https://github.com/RogueEdit/

from typing import Dict, Optional, List
from enum import Enum, auto

class Nature(Enum):
    HARDY = auto()
    LONELY = auto()
    BRAVE = auto()
    ADAMANT = auto()
    NAUGHTY = auto()
    BOLD = auto()
    DOCILE = auto()
    RELAXED = auto()
    IMPISH = auto()
    LAX = auto()
    TIMID = auto()
    HASTY = auto()
    SERIOUS = auto()
    JOLLY = auto()
    NAIVE = auto()
    MODEST = auto()
    MILD = auto()
    QUIET = auto()
    BASHFUL = auto()
    RASH = auto()
    CALM = auto()
    GENTLE = auto()
    SASSY = auto()
    CAREFUL = auto()
    QUIRKY = auto()
    UNLOCK_ALL = auto()  # New member for "Unlock All"

class NatureIDGenerator:
    """
    A class for generating nature names and IDs, and retrieving the ID for the 'unlock_all' nature.
    """

    def __init__(self, nature_names: Optional[List[str]] = None) -> None:
        """
        Initialize the NatureIDGenerator object.

        Args:
            nature_names (Optional[List[str]]): Optional list of nature names as strings. If provided, it will be used to initialize
            self.nature_names. If not provided, all names from the Nature enum will be used.
        """
        if nature_names is not None:
            self.nature_names: List[str] = nature_names
        else:
            self.nature_names: List[str] = [nature.name for nature in Nature if nature != Nature.UNLOCK_ALL]
        self.nature_ids: List[int] = [2 ** i for i in range(1, len(self.nature_names) + 1)]
        self.max_id: int = 2  # Start with ID 2

    def generate_nature_id_dict(self) -> Dict[str, int]:
        """
        Generate nature names and IDs and return them as a dictionary.

        Returns:
            Dict[str, int]: A dictionary containing nature names as keys and their corresponding IDs as values.
        """
        nature_dict: Dict[str, int] = {}
        for nature_name, nature_id in zip(self.nature_names, self.nature_ids):
            nature_dict[nature_name] = nature_id

        # Add 'unlock_all' nature to the dictionary
        nature_dict['Unlock all Natures'] = self.nature_ids[-1] * 2

        return nature_dict

    def generate_enum_id_dict(self) -> Dict[Nature, int]:
        """
        Generate nature IDs and return them as a dictionary with Nature enum members as keys.

        Returns:
            Dict[Nature, int]: A dictionary containing Nature enum members as keys and their corresponding IDs as values.
        """
        enum_id_dict: Dict[Nature, int] = {}
        for nature, nature_id in zip(Nature, self.nature_ids + [self.nature_ids[-1] * 2]):
            enum_id_dict[nature] = nature_id

        return enum_id_dict

    def get_unlock_all_nature_ids(self) -> Optional[int]:
        """
        Get the ID for the 'unlock_all' nature.

        Returns:
            Optional[int]: The ID for the 'unlock_all' nature, or None if not found.
        """
        enum_id_dict = self.generate_enum_id_dict()
        return enum_id_dict.get(Nature.UNLOCK_ALL, None)

#custom_names = ["ADAMANT", "TEST"]
#generator = NatureIDGenerator(custom_names)

# Example usage without custom list of nature names
generator = NatureIDGenerator()

# Generate full list of nature names and IDs as a dictionary
nature_dict = generator.generate_nature_id_dict()
print(nature_dict)

# Generate a dictionary with Nature enum members and their corresponding IDs
enum_id_dict = generator.generate_enum_id_dict()
print("\nEnum to ID dictionary:")
for nature, nature_id in enum_id_dict.items():
    print(f"{nature}: {nature_id}")

# Get value for 'unlock_all' nature
unlock_all_value = generator.get_unlock_all_nature_ids()
print("\nValue for 'unlock_all' nature:", unlock_all_value)

# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 04.06.2024 



from typing import Optional, List
from enum import Enum, auto
import json
import os

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
    UNLOCK_ALL = auto()


class NatureSlot(Enum):
    NATURE_SLOT = {
        "HARDY": 0,
        "LONELY": 1,
        "BRAVE": 2,
        "ADAMANT": 3,
        "NAUGHTY": 4,
        "BOLD": 5,
        "DOCILE": 6,
        "RELAXED": 7,
        "IMPISH": 8,
        "LAX": 9,
        "TIMID": 10,
        "HASTY": 11,
        "SERIOUS": 12,
        "JOLLY": 13,
        "NAIVE": 14,
        "MODEST": 15,
        "MILD": 16,
        "QUIET": 17,
        "BASHFUL": 18,
        "RASH": 19,
        "CALM": 20,
        "GENTLE": 21,
        "SASSY": 22,
        "CAREFUL": 23,
        "QUIRKY": 24
    }

class NoPassive(Enum):
    NO_PASSIVE_DICT = {
        "25": "25",
        "35": "35",
        "39": "39",
        "106": "106",
        "107": "107",
        "113": "113",
        "122": "122",
        "124": "124",
        "125": "125",
        "126": "126",
        "143": "143",
        "183": "183",
        "185": "185",
        "202": "202",
        "226": "226",
        "315": "315",
        "358": "358",
        "4122": "4122"
    }

class Biome(Enum):
    BIOMES_DICT = {
        "TOWN": "0",
        "PLAINS": "1",
        "GRASS": "2",
        "TALL_GRASS": "3",
        "METROPOLIS": "4",
        "FOREST": "5",
        "SEA": "6",
        "SWAMP": "7",
        "BEACH": "8",
        "LAKE": "9",
        "SEABED": "10",
        "MOUNTAIN": "11",
        "BADLANDS": "12",
        "CAVE": "13",
        "DESERT": "14",
        "ICE_CAVE": "15",
        "MEADOW": "16",
        "POWER_PLANT": "17",
        "VOLCANO": "18",
        "GRAVEYARD": "19",
        "DOJO": "20",
        "FACTORY": "21",
        "RUINS": "22",
        "WASTELAND": "23",
        "ABYSS": "24",
        "SPACE": "25",
        "CONSTRUCTION_SITE": "26",
        "JUNGLE": "27",
        "FAIRY_CAVE": "28",
        "TEMPLE": "29",
        "SLUM": "30",
        "SNOWY_FOREST": "31",
        "ISLAND": "40",
        "LABORATORY": "33",
        "END": "50"
    }


class Vouchers(Enum):
    VOUCHERS_DICT = {
    "CLASSIC_VICTORY": 1,
        "BROCK": 2,
        "MISTY": 3,
        "LT_SURGE": 4,
        "ERIKA": 5,
        "JANINE": 6,
        "SABRINA": 7,
        "BLAINE": 8,
        "GIOVANNI": 9,
        "FALKNER": 10,
        "BUGSY": 11,
        "WHITNEY": 12,
        "MORTY": 13,
        "CHUCK": 14,
        "JASMINE": 15,
        "PRYCE": 16,
        "CLAIR": 17,
        "ROXANNE": 18,
        "BRAWLY": 19,
        "WATTSON": 20,
        "FLANNERY": 21,
        "NORMAN": 22,
        "WINONA": 23,
        "TATE": 24,
        "LIZA": 25,
        "JUAN": 26,
        "ROARK": 27,
        "GARDENIA": 28,
        "MAYLENE": 29,
        "CRASHER_WAKE": 30,
        "FANTINA": 31,
        "BYRON": 32,
        "CANDICE": 33,
        "VOLKNER": 34,
        "CILAN": 35,
        "CHILI": 36,
        "CRESS": 37,
        "CHEREN": 38,
        "LENORA": 39,
        "ROXIE": 40,
        "BURGH": 41,
        "ELESA": 42,
        "CLAY": 43,
        "SKYLA": 44,
        "BRYCEN": 45,
        "DRAYDEN": 46,
        "MARLON": 47,
        "VIOLA": 48,
        "GRANT": 49,
        "KORRINA": 50,
        "RAMOS": 51,
        "CLEMONT": 52,
        "VALERIE": 53,
        "OLYMPIA": 54,
        "WULFRIC": 55,
        "MILO": 56,
        "NESSA": 57,
        "KABU": 58,
        "BEA": 59,
        "ALLISTER": 60,
        "OPAL": 61,
        "BEDE": 62,
        "GORDIE": 63,
        "MELONY": 64,
        "PIERS": 65,
        "MARNIE": 66,
        "RAIHAN": 67,
        "KATY": 68,
        "BRASSIUS": 69,
        "IONO": 70,
        "KOFU": 71,
        "LARRY": 72,
        "RYME": 73,
        "TULIP": 74,
        "GRUSHA": 75,
        "LORELEI": 76,
        "BRUNO": 77,
        "AGATHA": 78,
        "LANCE": 79,
        "WILL": 80,
        "KOGA": 81,
        "KAREN": 82,
        "SIDNEY": 83,
        "PHOEBE": 84,
        "GLACIA": 85,
        "DRAKE": 86,
        "AARON": 87,
        "BERTHA": 88,
        "FLINT": 89,
        "LUCIAN": 90,
        "SHAUNTAL": 91,
        "MARSHAL": 92,
        "GRIMSLEY": 93,
        "CAITLIN": 94,
        "MALVA": 95,
        "SIEBOLD": 96,
        "WIKSTROM": 97,
        "DRASNA": 98,
        "HALA": 99,
        "MOLAYNE": 100,
        "OLIVIA": 101,
        "ACEROLA": 102,
        "KAHILI": 103,
        "MARNIE_ELITE": 104,
        "NESSA_ELITE": 105,
        "BEA_ELITE": 106,
        "ALLISTER_ELITE": 107,
        "RAIHAN_ELITE": 108,
        "RIKA": 109,
        "POPPY": 110,
        "LARRY_ELITE": 111,
        "HASSEL": 112,
        "CRISPIN": 113,
        "AMARYS": 114,
        "LACEY": 115,
        "DRAYTON": 116,
        "BLUE": 117,
        "RED": 118,
        "LANCE_CHAMPION": 119,
        "STEVEN": 120,
        "WALLACE": 121,
        "CYNTHIA": 122,
        "ALDER": 123,
        "IRIS": 124,
        "DIANTHA": 125,
        "HAU": 126,
        "LEON": 127,
        "GEETA": 128,
        "NEMONA": 129,
        "KIERAN": 130
    }


class Generator:
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
            self.nature_names: List[str] = [nature.name for nature in Nature]  # Include all natures
        self.nature_ids: List[int] = [2 ** i for i in range(1, len(self.nature_names) + 1)]  # Start with ID 2
        self.max_id: int = max(self.nature_ids)  # Calculate max ID



    
    def __nature_to_json(self) -> str:
        """
            Dumps to json the natures IDs.
        """
        nature_dict: dict = {name: id for name, id in zip(self.nature_names, self.nature_ids)}
        return json.dumps({"natures": nature_dict}, indent=4)
    
    def __generate_no_passive_json(self) -> str:
        """
            Dumps to json the pokemon IDs wothout passive.
        """
        return json.dumps({"noPassive": NoPassive.NO_PASSIVE_DICT.value}, indent=4)
    
    def __generate_biomes_json(self) -> str:
        """
            Dumps to json the biomes IDs.
        """
        return json.dumps({"biomes": Biome.BIOMES_DICT.value}, indent=4)
    
    def __generate_vouchers_json(self) -> str:
        return json.dumps({"vouchers": Vouchers.VOUCHERS_DICT.value}, indent=4)
    
    def __natureSlot_to_json(self) -> str:
        return json.dumps({"natureSlot": NatureSlot.NATURE_SLOT.value}, indent=4)
    
    def __save_to_file(self, data: str, filename: str) -> None:
        directory: str = "./data/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath: os.path = os.path.join(directory, filename)
        with open(filepath, "w") as file:
            file.write(data)
    
    def generate(self) -> None:
        nature_json: str = self.__nature_to_json()
        self.__save_to_file(nature_json, "natures.json")

        no_passive_json: str = self.__generate_no_passive_json()
        self.__save_to_file(no_passive_json, "passive.json")

        biomes_json: str = self.__generate_biomes_json()
        self.__save_to_file(biomes_json, "biomes.json")

        vouchers_json: str = self.__generate_vouchers_json()
        self.__save_to_file(vouchers_json, "vouchers.json")

        natureSlot: str = self.__natureSlot_to_json()
        self.__save_to_file(natureSlot, "natureSlot.json")

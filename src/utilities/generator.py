# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood
# Date of release: 06.06.2024
# Last Edited: 25.06.2024
# Based on: https://github.com/pagefaultgames/pokerogue/

"""
This script provides a generator for creating JSON files from various enums representing natures, no passive Pokemon, biomes, vouchers, and nature slots. It includes functionality to save these JSON files to disk.

Features:
- Convert enum data to JSON strings.
- Save JSON data to files.
- Handle directories and file operations.

Modules:
- typing: Provides type hints for function signatures and variable declarations.
- enum: Provides support for enumerations, a set of symbolic names bound to unique, constant values.
- json: Provides functionalities to work with JSON data for reading and writing.
- os: Provides a way to interact with the operating system, particularly for file and directory operations.
- utilities: Custom module for colored printing and logging functionalities.

Workflow:
1. Define enums for various categories (natures, no passive, biomes, vouchers, nature slots).
2. Initialize the Generator class with optional nature names.
3. Generate JSON strings from the enums.
4. Save JSON data to files.
"""

from typing import Optional, List
# Provides type hints for function signatures and variable declarations.

from enum import Enum, auto
# Provides support for enumerations, a set of symbolic names bound to unique, constant values.

import json
# Provides functionalities to work with JSON data for reading and writing.

import os
# Provides a way to interact with the operating system, particularly for file and directory operations.

from utilities import cFormatter, Color
# Custom module for colored printing and logging functionalities.

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
        'HARDY': 0,
        'LONELY': 1,
        'BRAVE': 2,
        'ADAMANT': 3,
        'NAUGHTY': 4,
        'BOLD': 5,
        'DOCILE': 6,
        'RELAXED': 7,
        'IMPISH': 8,
        'LAX': 9,
        'TIMID': 10,
        'HASTY': 11,
        'SERIOUS': 12,
        'JOLLY': 13,
        'NAIVE': 14,
        'MODEST': 15,
        'MILD': 16,
        'QUIET': 17,
        'BASHFUL': 18,
        'RASH': 19,
        'CALM': 20,
        'GENTLE': 21,
        'SASSY': 22,
        'CAREFUL': 23,
        'QUIRKY': 24
    }

class NoPassive(Enum):
    NO_PASSIVE_DICT = {
        '25': '25',
        '35': '35',
        '39': '39',
        '106': '106',
        '107': '107',
        '113': '113',
        '122': '122',
        '124': '124',
        '125': '125',
        '126': '126',
        '143': '143',
        '183': '183',
        '185': '185',
        '202': '202',
        '226': '226',
        '315': '315',
        '358': '358',
        '4122': '4122'
    }

class Biome(Enum):
    BIOMES_DICT = {
        'TOWN': '0',
        'PLAINS': '1',
        'GRASS': '2',
        'TALL_GRASS': '3',
        'METROPOLIS': '4',
        'FOREST': '5',
        'SEA': '6',
        'SWAMP': '7',
        'BEACH': '8',
        'LAKE': '9',
        'SEABED': '10',
        'MOUNTAIN': '11',
        'BADLANDS': '12',
        'CAVE': '13',
        'DESERT': '14',
        'ICE_CAVE': '15',
        'MEADOW': '16',
        'POWER_PLANT': '17',
        'VOLCANO': '18',
        'GRAVEYARD': '19',
        'DOJO': '20',
        'FACTORY': '21',
        'RUINS': '22',
        'WASTELAND': '23',
        'ABYSS': '24',
        'SPACE': '25',
        'CONSTRUCTION_SITE': '26',
        'JUNGLE': '27',
        'FAIRY_CAVE': '28',
        'TEMPLE': '29',
        'SLUM': '30',
        'SNOWY_FOREST': '31',
        'ISLAND': '40',
        'LABORATORY': '33',
        'END': '50'
    }

class Vouchers(Enum):
    VOUCHERS_DICT = {
        'CLASSIC_VICTORY': 1,
        'BROCK': 2,
        'MISTY': 3,
        'LT_SURGE': 4,
        'ERIKA': 5,
        'JANINE': 6,
        'SABRINA': 7,
        'BLAINE': 8,
        'GIOVANNI': 9,
        'FALKNER': 10,
        'BUGSY': 11,
        'WHITNEY': 12,
        'MORTY': 13,
        'CHUCK': 14,
        'JASMINE': 15,
        'PRYCE': 16,
        'CLAIR': 17,
        'ROXANNE': 18,
        'BRAWLY': 19,
        'WATTSON': 20,
        'FLANNERY': 21,
        'NORMAN': 22,
        'WINONA': 23,
        'TATE': 24,
        'LIZA': 25,
        'JUAN': 26,
        'ROARK': 27,
        'GARDENIA': 28,
        'MAYLENE': 29,
        'CRASHER_WAKE': 30,
        'FANTINA': 31,
        'BYRON': 32,
        'CANDICE': 33,
        'VOLKNER': 34,
        'CILAN': 35,
        'CHILI': 36,
        'CRESS': 37,
        'CHEREN': 38,
        'LENORA': 39,
        'ROXIE': 40,
        'BURGH': 41,
        'ELESA': 42,
        'CLAY': 43,
        'SKYLA': 44,
        'BRYCEN': 45,
        'DRAYDEN': 46,
        'MARLON': 47,
        'VIOLA': 48,
        'GRANT': 49,
        'KORRINA': 50,
        'RAMOS': 51,
        'CLEMONT': 52,
        'VALERIE': 53,
        'OLYMPIA': 54,
        'WULFRIC': 55,
        'MILO': 56,
        'NESSA': 57,
        'KABU': 58,
        'BEA': 59,
        'ALLISTER': 60,
        'OPAL': 61,
        'BEDE': 62,
        'GORDIE': 63,
        'MELONY': 64,
        'PIERS': 65,
        'MARNIE': 66,
        'RAIHAN': 67,
        'KATY': 68,
        'BRASSIUS': 69,
        'IONO': 70,
        'KOFU': 71,
        'LARRY': 72,
        'RYME': 73,
        'TULIP': 74,
        'GRUSHA': 75,
        'LORELEI': 76,
        'BRUNO': 77,
        'AGATHA': 78,
        'LANCE': 79,
        'WILL': 80,
        'KOGA': 81,
        'KAREN': 82,
        'SIDNEY': 83,
        'PHOEBE': 84,
        'GLACIA': 85,
        'DRAKE': 86,
        'AARON': 87,
        'BERTHA': 88,
        'FLINT': 89,
        'LUCIAN': 90,
        'SHAUNTAL': 91,
        'MARSHAL': 92,
        'GRIMSLEY': 93,
        'CAITLIN': 94,
        'MALVA': 95,
        'SIEBOLD': 96,
        'WIKSTROM': 97,
        'DRASNA': 98,
        'HALA': 99,
        'MOLAYNE': 100,
        'OLIVIA': 101,
        'ACEROLA': 102,
        'KAHILI': 103,
        'MARNIE_ELITE': 104,
        'NESSA_ELITE': 105,
        'BEA_ELITE': 106,
        'ALLISTER_ELITE': 107,
        'RAIHAN_ELITE': 108,
        'RIKA': 109,
        'POPPY': 110,
        'LARRY_ELITE': 111,
        'HASSEL': 112,
        'CRISPIN': 113,
        'AMARYS': 114,
        'LACEY': 115,
        'DRAYTON': 116,
        'BLUE': 117,
        'RED': 118,
        'LANCE_CHAMPION': 119,
        'STEVEN': 120,
        'WALLACE': 121,
        'CYNTHIA': 122,
        'ALDER': 123,
        'IRIS': 124,
        'DIANTHA': 125,
        'HAU': 126,
        'LEON': 127,
        'GEETA': 128,
        'NEMONA': 129,
        'KIERAN': 130,
        'ROCKET_BOSS_GIOVANNI_1': 131,
        'ROCKET_BOSS_GIOVANNI_2': 132,
        'MAXIE': 133,
        'MAXIE_2': 134,
        'ARCHIE': 135,
        'ARCHIE_2': 136,
        'CYRUS': 137,
        'CYRUS_2': 138,
        'GHETSIS': 139,
        'GHETSIS_2': 140,
        'LYSANDRE': 141,
        'LYSANDRE_2': 142
    }

class Achievements(Enum):
    ACHIEVEMENTS_DICT = {
        '_10K_MONEY': 1,
        '_100K_MONEY': 2,
        '_1M_MONEY': 3,
        '_10M_MONEY': 4,
        '_250_DMG': 5,
        '_1000_DMG': 6,
        '_2500_DMG': 7,
        '_10000_DMG': 8,
        '_250_HEAL': 9,
        '_1000_HEAL': 10,
        '_2500_HEAL': 11,
        '_10000_HEAL': 12,
        'LV_100': 13,
        'LV_250': 14,
        'LV_1000': 15,
        '_10_RIBBONS': 16,
        '_25_RIBBONS': 17,
        '_50_RIBBONS': 18,
        '_75_RIBBONS': 19,
        '_100_RIBBONS': 20,
        'TRANSFER_MAX_BATTLE_STAT': 21,
        'MAX_FRIENDSHIP': 22,
        'MEGA_EVOLVE': 23,
        'GIGANTAMAX': 24,
        'TERASTALLIZE': 25,
        'STELLAR_TERASTALLIZE': 26,
        'SPLICE': 27,
        'MINI_BLACK_HOLE': 28,
        'CATCH_MYTHICAL': 29,
        'CATCH_SUB_LEGENDARY': 30,
        'CATCH_LEGENDARY': 31,
        'SEE_SHINY': 32,
        'SHINY_PARTY': 33,
        'HATCH_MYTHICAL': 34,
        'HATCH_SUB_LEGENDARY': 35,
        'HATCH_LEGENDARY': 36,
        'HATCH_SHINY': 37,
        'HIDDEN_ABILITY': 38,
        'PERFECT_IVS': 39,
        'CLASSIC_VICTORY': 40,
        'MONO_GEN_ONE_VICTORY': 41,
        'MONO_GEN_TWO_VICTORY': 42,
        'MONO_GEN_THREE_VICTORY': 43,
        'MONO_GEN_FOUR_VICTORY': 44,
        'MONO_GEN_FIVE_VICTORY': 45,
        'MONO_GEN_SIX_VICTORY': 46,
        'MONO_GEN_SEVEN_VICTORY': 47,
        'MONO_GEN_EIGHT_VICTORY': 48,
        'MONO_GEN_NINE_VICTORY': 49,
        'MONO_NORMAL': 50,
        'MONO_FIGHTING': 51,
        'MONO_FLYING': 52,
        'MONO_POISON': 53,
        'MONO_GROUND': 54,
        'MONO_ROCK': 55,
        'MONO_BUG': 56,
        'MONO_GHOST': 57,
        'MONO_STEEL': 58,
        'MONO_FIRE': 59,
        'MONO_WATER': 60,
        'MONO_GRASS': 61,
        'MONO_ELECTRIC': 62,
        'MONO_PSYCHIC': 63,
        'MONO_ICE': 64,
        'MONO_DRAGON': 65,
        'MONO_DARK': 66,
        'MONO_FAIRY': 67
    }

class Generator:
    def __init__(self, nature_names: Optional[List[str]] = None) -> None:
        """
        Initialize the Generator object.

        Args:
            nature_names (Optional[List[str]]): Optional list of nature names as strings. If provided, it will be used to initialize
            self.nature_names. If not provided, all names from the Nature enum will be used.

        Modules:
            - typing: Provides type hints for function signatures and variable declarations.
        """
        if nature_names is not None:
            self.nature_names: List[str] = nature_names
        else:
            self.nature_names: List[str] = [nature.name for nature in Nature]  # Include all natures
        self.nature_ids: List[int] = [2 ** i for i in range(1, len(self.nature_names) + 1)]

        # Reduce the last ID by 2
        if len(self.nature_ids) > 0:
            self.nature_ids[-1] -= 2

        self.max_id: int = max(self.nature_ids)  # Calculate max ID

    def __nature_to_json(self) -> str:
        nature_dict: dict = {name: id for name, id in zip(self.nature_names, self.nature_ids)}
        return json.dumps({'natures': nature_dict}, indent=4)
    
    def __generate_no_passive_json(self) -> str:
        return json.dumps({'noPassive': NoPassive.NO_PASSIVE_DICT.value}, indent=4)
    
    def __generate_biomes_json(self) -> str:
        return json.dumps({'biomes': Biome.BIOMES_DICT.value}, indent=4)
    
    def __generate_vouchers_json(self) -> str:
        return json.dumps({'vouchers': Vouchers.VOUCHERS_DICT.value}, indent=4)
    
    def __natureSlot_to_json(self) -> str:
        return json.dumps({'natureSlot': NatureSlot.NATURE_SLOT.value}, indent=4)
    
    def __achievments_to_json(self) -> str:
        return json.dumps({'achvUnlocks': Achievements.ACHIEVEMENTS_DICT.value}, indent=4)
    
    def __save_to_file(self, data: str, filename: str) -> None:
        """
        Save data to a file.

        Args:
            data (str): The data to be saved.
            filename (str): The name of the file.

        Example:
            __save_to_file('{"key": "value"}', 'example.json')

        Modules:
            - os: Provides a way to interact with the operating system, particularly for file and directory operations.
            - utilities: Custom module for colored printing and logging functionalities.
        """
        try:
            directory: str = './data/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            filepath: os.path = os.path.join(directory, filename)
            with open(filepath, 'w') as file:
                file.write(data)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Something went wrong. {e}', isLogging=True)
    
    def generate(self) -> None:
        """
        Generate and save various JSON files for natures, no passives, biomes, vouchers, and nature slots.

        Example:
            generator = Generator()
            generator.generate()

        Modules:
            - json: Provides functionalities to work with JSON data for reading and writing.
            - os: Provides a way to interact with the operating system, particularly for file and directory operations.
            - utilities: Custom module for colored printing and logging functionalities.
        """
        try:
            nature_json: str = self.__nature_to_json()
            self.__save_to_file(nature_json, 'natures.json')

            no_passive_json: str = self.__generate_no_passive_json()
            self.__save_to_file(no_passive_json, 'passive.json')

            biomes_json: str = self.__generate_biomes_json()
            self.__save_to_file(biomes_json, 'biomes.json')

            vouchers_json: str = self.__generate_vouchers_json()
            self.__save_to_file(vouchers_json, 'vouchers.json')

            natureSlot: str = self.__natureSlot_to_json()
            self.__save_to_file(natureSlot, 'natureSlot.json')

            achvs: str = self.__achievments_to_json()
            self.__save_to_file(achvs, 'achievements.json')

        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Generating data on initializing startup failed. {e}', isLogging=True)
# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood, https://github.com/JulianStiebler
# Date of release: 06.06.2024
# Last edited: 20.06.2024

"""
This script provides functionalities to load data from JSON files and convert them into Enums.
It includes the capability to handle Pokemon IDs, biomes, moves, natures, vouchers, and nature slots.

Modules:
- utilities: Custom module for colored printing and logging functionalities (cFormatter and Color).
- modules: Contains configuration settings (config).
- json: Provides functionalities to work with JSON data.
- enum: Provides support for enumerations, a set of symbolic names bound to unique, constant values.

Workflow:
1. Initialize the EnumLoader class.
2. Load data from JSON files located in a specified directory.
3. Convert loaded data to Enums.
4. Return the created Enums.
"""

from utilities import cFormatter, Color
# Custom module for colored printing and logging functionalities.

from modules import config
# Contains configuration settings, specifically for directory paths.

import json
# Provides functionalities to work with JSON data for reading and writing.

from enum import Enum
# Provides support for enumerations, a set of symbolic names bound to unique, constant values.

from typing import Optional, Tuple, Dict
# Provides type hints for better code clarity and type checking.

class EnumLoader:
    def __init__(self) -> None:
        """
        Initialize the EnumLoader object.

        Attributes:
            pokemon_id_by_name (Optional[dict]): Dictionary for Pokemon IDs by name.
            pokemon_name_by_id (Optional[dict]): Dictionary for Pokemon names by ID.
            biomes_by_id (Optional[dict]): Dictionary for biomes by ID.
            move_id_by_name (Optional[dict]): Dictionary for move IDs by name.
            move_name_by_id: Optional[dict]): Dictionary for move names by ID.
            natures_data (Optional[dict]): Dictionary for natures data.
            vouchers_data (Optional[dict]): Dictionary for vouchers data.
            natureSlot_data (Optional[dict]): Dictionary for nature slot data.

        Modules:
            - typing: Provides type hints for better code clarity and type checking.
        """
        self.pokemon_id_by_name: Optional[Dict[str, int]] = None
        self.pokemon_name_by_id: Optional[Dict[int, str]] = None
        self.biomes_by_id: Optional[Dict[str, int]] = None
        self.move_id_by_name: Optional[Dict[str, int]] = None
        self.move_name_by_id: Optional[Dict[int, str]] = None
        self.natures_data: Optional[Dict[str, int]] = None
        self.vouchers_data: Optional[Dict[str, int]] = None
        self.natureSlot_data: Optional[Dict[str, int]] = None

    def __load_data(self) -> None:
        """
        Load data from JSON files located in the directory specified by config.data_directory.

        Raises:
            Exception: If there is an error loading the data files.

        Example:
            loader = EnumLoader()
            loader.__load_data()

        Modules:
            - json: Provides functionalities to work with JSON data for reading and writing.
            - modules.config: Contains configuration settings, specifically for directory paths.
            - utilities.cFormatter: Custom formatter for colored printing and logging.
        """
        try:
            data_dir: str = config.data_directory
            with open(f'{data_dir}/pokemon.json') as f:
                self.pokemon_id_by_name = json.load(f)['dex']

            self.pokemon_name_by_id = {v: k for k, v in self.pokemon_id_by_name.items()}

            with open(f'{data_dir}/biomes.json') as f:
                self.biomes_by_id = json.load(f)['biomes']

            with open(f'{data_dir}/moves.json') as f:
                self.move_id_by_name = json.load(f)['moves']

            self.move_name_by_id = {v: k for k, v in self.move_id_by_name.items()}

            with open(f'{data_dir}/natures.json') as f:
                self.natures_data = json.load(f)['natures']

            with open(f'{data_dir}/vouchers.json') as f:
                self.vouchers_data = json.load(f)['vouchers']
            
            with open(f'{data_dir}/natureSlot.json') as f:
                self.natureSlot_data = json.load(f)['natureSlot']
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in enumLoader.__load_data(). {e}', isLogging=True)

    def __create_enum_from_dict(self, data_dict: Dict[str, int], enum_name: str) -> Enum:
        """
        Create an Enum from a dictionary.

        Args:
            data_dict (dict): The dictionary to convert to an Enum.
            enum_name (str): The name of the Enum.

        Returns:
            Enum: The created Enum.

        Example:
            loader = EnumLoader()
            pokemon_enum = loader.__create_enum_from_dict({'PIKACHU': 25}, 'PokemonEnum')

        Modules:
            - enum: Provides support for enumerations, a set of symbolic names bound to unique, constant values.
        """
        enum_cls: Enum = Enum(enum_name, {key: value for key, value in data_dict.items()})
        return enum_cls

    def convert_to_enums(self) -> Tuple[Enum, Enum, Enum, Enum, Enum, Enum]:
        """
        Convert loaded data to Enums.

        Returns:
            tuple: A tuple containing the created Enums for Pokemon IDs, biomes, moves, natures, vouchers, and nature slots.

        Example:
            loader = EnumLoader()
            enums = loader.convert_to_enums()
            pokemon_enum = enums[0]  # Access PokemonEnum

        Modules:
            - json: Provides functionalities to work with JSON data for reading and writing.
            - enum: Provides support for enumerations, a set of symbolic names bound to unique, constant values.
            - modules.config: Contains configuration settings, specifically for directory paths.
            - utilities.cFormatter: Custom formatter for colored printing and logging.
        """
        self.__load_data()

        self.pokemon_id_by_name = self.__create_enum_from_dict(self.pokemon_id_by_name, 'PokemonEnum')
        self.pokemon_name_by_id = self.__create_enum_from_dict(self.pokemon_name_by_id, 'PokemonIdEnum')
        self.biomes_by_id = self.__create_enum_from_dict(self.biomes_by_id, 'BiomesEnum')
        self.move_id_by_name = self.__create_enum_from_dict(self.move_id_by_name, 'MovesEnum')
        self.move_name_by_id = self.__create_enum_from_dict(self.move_name_by_id, 'MoveIdEnum')
        self.natures_data = self.__create_enum_from_dict(self.natures_data, 'NaturesEnum')
        self.vouchers_data = self.__create_enum_from_dict(self.vouchers_data, 'VouchersEnum')
        self.natureSlot_data = self.__create_enum_from_dict(self.natureSlot_data, 'NaturesSlotEnum')

        return (self.pokemon_id_by_name, self.pokemon_name_by_id, self.biomes_by_id, self.move_id_by_name, self.move_name_by_id, self.natures_data, self.vouchers_data, self.natureSlot_data)

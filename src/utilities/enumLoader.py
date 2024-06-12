# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/claudiunderthehood https://github.com/JulianStiebler/
# Date of release: 06.06.2024 

from utilities.cFormatter import cFormatter, Color
import json

from enum import Enum

class EnumLoader:
    def __init__(self):
        """
        Initialize the EnumLoader object.
        """
        self.pokemon_id_by_name = None
        self.biomes_by_id = None
        self.moves_by_id = None
        self.natures_data = None
        self.vouchers_data = None
        self.natureSlot_data = None

    def __load_data(self) -> None:
        """
        Load data from JSON files.
        """
        try:
            with open('./data/pokemon.json') as f:
                self.pokemon_id_by_name = json.load(f)

            with open('./data/biomes.json') as f:
                self.biomes_by_id = json.load(f)

            with open('./data/moves.json') as f:
                self.moves_by_id = json.load(f)

            with open('./data/natures.json') as f:
                self.natures_data = json.load(f)

            with open('./data/vouchers.json') as f:
                self.vouchers_data = json.load(f)
            
            with open('./data/natureSlot.json') as f:
                self.natureSlot_data = json.load(f)
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Error in enumLoader.__load_data(). {e}', isLogging=True)

    def __create_enum_from_dict(self, data_dict: dict, enum_name: str) -> Enum:
        """
        Create an Enum from a dictionary.

        Args:
            data_dict (dict): The dictionary to convert to an Enum.
            enum_name (str): The name of the Enum.

        Returns:
            Enum: The created Enum.
        """
        enum_cls = Enum(enum_name, {key: value for key, value in data_dict.items()})
        return enum_cls

    def convert_to_enums(self) -> tuple:
        """
        Convert loaded data to Enums.

        Returns:
            tuple: A tuple containing the created Enums.
        """
        self.__load_data()

        self.pokemon_id_by_name = self.__create_enum_from_dict(self.pokemon_id_by_name['dex'], 'PokemonEnum')
        self.biomes_by_id = self.__create_enum_from_dict(self.biomes_by_id['biomes'], 'BiomesEnum')
        self.moves_by_id = self.__create_enum_from_dict(self.moves_by_id['moves'], 'MovesEnum')
        self.natures_data = self.__create_enum_from_dict(self.natures_data['natures'], 'NaturesEnum')
        self.vouchers_data = self.__create_enum_from_dict(self.vouchers_data['vouchers'], 'VouchersEnum')
        self.natureSlot_data = self.__create_enum_from_dict(self.natureSlot_data['natureSlot'], 'NaturesSlotEnum')

        return self.pokemon_id_by_name, self.biomes_by_id, self.moves_by_id, self.natures_data, self.vouchers_data, self.natureSlot_data
# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 13.06.2024 
# Last Edited: 22.06.2024

# Unlike the other code, reusing this in your own project is forbidden.

import os
import json
from typing import Any, List, Optional, Dict

# Define the Modifier class
class Modifier:
    def __init__(self, args: Optional[List[Any]], className: str, player: bool, stackCount: int, typeId: str, typePregenArgs: Optional[List[Any]] = None):
        self.args = self._sanitize_values(args)
        self.className = className
        self.player = player
        self.stackCount = stackCount
        self.typeId = typeId
        self.typePregenArgs = self._sanitize_values(typePregenArgs)

    def _sanitize_values(self, values: Optional[List[Any]]) -> Optional[List[Any]]:
        if values is None:
            return None
        return [None if (isinstance(v, (int, float)) and v > 30) else v for v in values]

    def to_dict(self) -> dict:
        data = {
            'args': self.args,
            'className': self.className,
            'player': self.player,
            'stackCount': self.stackCount,
            'typeId': self.typeId
        }
        if self.typePregenArgs is not None:
            data['typePregenArgs'] = self.typePregenArgs
        return data

    def to_python_code(self, unique_name: str) -> str:
        args_str = "None" if self.args is None else repr(self.args)
        typePregenArgs_str = "" if self.typePregenArgs is None else f", typePregenArgs={repr(self.typePregenArgs)}"
        return f"{unique_name} = Modifier(args={args_str}, className={repr(self.className)}, player={self.player}, stackCount={self.stackCount}, typeId={repr(self.typeId)}{typePregenArgs_str})"

# Function to parse the game save file and extract modifiers
def parse_game_save(file_path: str) -> List[Modifier]:
    modifiers = []
    with open(file_path, 'r') as file:
        data = json.load(file)
        if 'modifiers' in data:
            for modifier_data in data['modifiers']:
                modifier = parse_modifier(modifier_data)
                if modifier:
                    modifiers.append(modifier)
        if 'EnemyModifiers' in data:
            for modifier_data in data['EnemyModifiers']:
                modifier = parse_modifier(modifier_data)
                if modifier:
                    modifiers.append(modifier)
    return modifiers

# Function to parse individual modifier data
def parse_modifier(data: dict) -> Optional[Modifier]:
    if 'typeId' in data and 'className' in data and 'player' in data and 'stackCount' in data:
        args = data.get('args', None)
        className = data['className']
        player = data['player']
        stackCount = data['stackCount']
        typeId = data['typeId']
        typePregenArgs = data.get('typePregenArgs', None)
        
        return Modifier(args=args, className=className, player=player, stackCount=stackCount, typeId=typeId, typePregenArgs=typePregenArgs)
    return None

# Function to save extracted modifiers data to a JSON file
def save_extracted_modifiers(modifiers: List[Modifier], output_file: str):
    data = [modifier.to_dict() for modifier in modifiers]
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Function to generate converted_.py with modifiers in Python code format
def generate_converted_py(modifiers: List[Modifier], output_file: str):
    unique_modifiers = {}
    for modifier in modifiers:
        typeId = modifier.typeId
        typePregenArgs = tuple(modifier.typePregenArgs) if modifier.typePregenArgs is not None else None
        if typeId not in unique_modifiers:
            unique_modifiers[typeId] = set()
        unique_modifiers[typeId].add(typePregenArgs)

    sorted_modifiers = []
    for typeId, typePregenArgs_set in unique_modifiers.items():
        for typePregenArgs in typePregenArgs_set:
            modifier = next(m for m in modifiers if m.typeId == typeId and (tuple(m.typePregenArgs) if m.typePregenArgs is not None else None) == typePregenArgs)
            unique_name = typeId.replace('-', '_').upper()
            if typePregenArgs is not None:
                unique_name += "".join(str(arg) for arg in typePregenArgs if arg is not None)
            sorted_modifiers.append((unique_name, modifier))

    sorted_modifiers.sort(key=lambda x: x[0])

    with open(output_file, 'w') as file:
        file.write("# This file contains converted modifiers\n")
        for unique_name, modifier in sorted_modifiers:
            file.write(modifier.to_python_code(unique_name) + "\n")

    print(f"Converted modifiers saved to '{output_file}'")

# Function to process all JSON files in the current directory
def process_all_json_files():
    current_dir = os.getcwd()
    json_files = [file for file in os.listdir(current_dir) if file.endswith('.json') and not file.startswith('extracted_')]

    for json_file in json_files:
        input_file = os.path.join(current_dir, json_file)
        extracted_output_file = os.path.join(current_dir, f"extracted_{json_file}")
        converted_output_file = os.path.join(current_dir, f"converted_{json_file.replace('.json', '.py')}")

        # Extract modifiers from input file
        modifiers = parse_game_save(input_file)

        # Save extracted modifiers to extracted_.json
        save_extracted_modifiers(modifiers, extracted_output_file)

        # Generate converted_.py with modifiers in Python code format
        generate_converted_py(modifiers, converted_output_file)

        print(f"Modifiers data extracted from '{json_file}', saved to '{extracted_output_file}', and converted to '{converted_output_file}'")

# Entry point of the script
def main():
    process_all_json_files()

if __name__ == "__main__":
    main()

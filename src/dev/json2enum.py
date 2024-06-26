import os
import json
from enum import Enum

def convert_json_to_enum(input_filepath: str, output_filepath: str, enum_class_name: str) -> None:
    """
    Converts a JSON file containing name-value pairs into an Enum class format and writes it to a Python file.

    Args:
    - input_filepath (str): Path to the input JSON file.
    - output_filepath (str): Path to the output Python file where the Enum class will be written.
    - enum_class_name (str): The name of the Enum class to be generated.
    """
    try:
        with open(input_filepath, 'r') as infile:
            data = json.load(infile)

        # Extracting the 'dex' dictionary from JSON data
        dex_dict = data.get('dex', {})

        # Generating the Enum members from dex_dict
        enum_members = {name.upper(): int(value) for name, value in dex_dict.items()}

        # Creating the Enum class dynamically
        EnumClass = Enum(enum_class_name, enum_members)

        # Generating the Python script content
        script_content = f"class {enum_class_name}(Enum):\n"
        script_content += f"    {enum_class_name}_DICT = {{\n"
        for name, value in enum_members.items():
            script_content += f"        '{name}': {value},\n"
        script_content += "    }\n"

        # Writing the script content to the output file
        with open(output_filepath, 'w') as outfile:
            outfile.write(script_content)

        print(f"Enum class '{enum_class_name}' successfully generated and saved to '{output_filepath}'.")

    except FileNotFoundError:
        print(f"Error: File '{input_filepath}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{input_filepath}'.")
    except Exception as e:
        print(f"Error: {e}")

def process_json_files(directory: str, output_directory: str) -> None:
    """
    Processes all JSON files in the given directory and converts them to Enum classes.

    Args:
    - directory (str): Directory containing JSON files to process.
    - output_directory (str): Directory where the generated Python scripts will be saved.
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Iterate over all JSON files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                input_filepath = os.path.join(directory, filename)
                output_filepath = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_enum.py")
                enum_class_name = os.path.splitext(filename)[0].title() + "Enum"  # Example: If filename is "data.json", enum class name will be "DataEnum"

                # Convert JSON file to Enum class
                convert_json_to_enum(input_filepath, output_filepath, enum_class_name)

    except Exception as e:
        print(f"Error processing JSON files: {e}")

# Example usage:
input_directory = '../../data/'
output_directory = '/converted/'

process_json_files(input_directory, output_directory)

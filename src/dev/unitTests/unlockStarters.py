import unittest
import json
import random
from pathlib import Path
from trainer_module import Trainer, handle_operation_exceptions
import unitTestModules as utm

class TestUnlockStarters(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test JSON files
        self.test_dir = Path('test_data')
        self.test_dir.mkdir(exist_ok=True)

        # Example JSON data for different scenarios
        self.example_data = {
            "dexData": {
                "entry1": {},
                "entry2": {}
            },
            "starterData": {
                "starter1": {},
                "starter2": {}
            }
        }
        self.empty_data = {
            "dexData": {},
            "starterData": {}
        }

        # Write example JSON files
        with open(self.test_dir / 'example1.json', 'w') as f:
            json.dump(self.example_data, f)
        with open(self.test_dir / 'example2.json', 'w') as f:
            json.dump(self.empty_data, f)

    def tearDown(self):
        # Remove temporary directory and files after tests
        for file in self.test_dir.iterdir():
            file.unlink()
        self.test_dir.rmdir()

    def test_unlock_starters(self):
        # Define the combinations of the first three inputs
        combinations = [
            ('1', '1', '1'),
            ('1', '1', '2'),
            ('1', '2', '1'),
            ('1', '2', '2'),
            ('2', '1', '1'),
            ('2', '1', '2'),
            ('2', '2', '1'),
            ('2', '2', '2'),
        ]

        # Iterate over each combination of inputs
        for choice1, choice2, choice3 in combinations:
            with self.subTest(choice1=choice1, choice2=choice2, choice3=choice3):
                # Setup mock return values for input functions
                utm.fh_getChoiceInput = lambda prompt, choices, zeroCancel=True: {
                    'Do you want to unlock all forms of the pokemon? (All forms are Tier 3 shinies)': choice1,
                    'Do you want Tier 3 shinies?': choice2,
                    'Do you want the starters to have perfect IVs?': choice3,
                    'Do you want to unlock all natures?': '1',
                    'Do you want the starters to have the passive unlocked?': '1',
                    'Do you want to unlock win-ribbons?': '1',
                    'How much do you want to reduce the cost? (0 for none)': '0',
                    'Do you want to unlock all abilities?': '1'
                }[prompt]

                utm.fh_getIntegerInput = lambda prompt, minVal, maxVal: 0

                # Mock JSON loading
                utm.fh_loadDataFromJSON = lambda filename: self.example_data

                # Initialize Trainer and call the method
                trainer = Trainer()
                trainer.f_unlockStarters()

                # Verify JSON was written correctly
                written_data = utm.fh_loadDataFromJSON('trainer.json')

                # Check if the dexData and starterData keys exist in the written data
                self.assertIn('dexData', written_data)
                self.assertIn('starterData', written_data)

if __name__ == '__main__':
    unittest.main()

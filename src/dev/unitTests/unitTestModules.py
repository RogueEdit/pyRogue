def fh_loadDataFromJSON(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def fh_writeJSONData(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def fh_getChoiceInput(prompt, choices, zeroCancel=False):
    # Simulate user input for testing purposes
    pass

def fh_getIntegerInput(prompt, minVal, maxVal):
    # Simulate user input for testing purposes
    pass

class cFormatter:
    @staticmethod
    def fh_centerText(text, width, fillchar):
        return text.center(width, fillchar)

    @staticmethod
    def print(color, text):
        print(text)

class Color:
    DEBUG = "debug"
    INFO = "info"

class OperationSuccessful(Exception):
    pass

# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Author
# Date of release: 25.06.2024
# Last Edited: 28.06.2024

from utilities import cFormatter, Color

# Initialize a global message buffer list
messageBuffer = []

# Function to clear the message buffer
def fh_clearMessageBuffer():
    global messageBuffer
    messageBuffer = []

# Function to append messages to the message buffer
def fh_appendMessageBuffer(type, message, isLogging=False):
    global messageBuffer
    messageBuffer.append((type, message, isLogging))

# Function to print messages from the message buffer
def fh_printMessageBuffer():
    global messageBuffer
    for color, text, isLogging in messageBuffer:
        if isinstance(color, Color):  # Check if color is a valid Color enum
            cFormatter.fh_centerText(text, length=55, fillChar='>')
            cFormatter.print(color, f'{text}', isLogging)
        else:
            print(text)
    messageBuffer = []  # Clear buffer after printing

from utilities import cFormatter, Color

# Initialize a global message buffer list
messageBuffer = []

# Function to clear the message buffer
def fh_clearMessageBuffer():
    global messageBuffer
    messageBuffer = []

# Function to append messages to the message buffer
def fh_appendMessageBuffer(type, message):
    global messageBuffer
    messageBuffer.append((type, message))

# Function to print messages from the message buffer
def fh_printMessageBuffer():
    global messageBuffer
    for color, text in messageBuffer:
        if isinstance(color, Color):  # Check if color is a valid Color enum
            cFormatter.fh_centerText(text, length=55, fillChar='>')
            cFormatter.print(color, f'{text}')
        else:
            print(text)
    messageBuffer = []  # Clear buffer after printing
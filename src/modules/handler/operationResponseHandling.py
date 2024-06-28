# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Author
# Date of release: 25.06.2024 
# Last Edited: 28.06.2024

from utilities import Color
from json import JSONDecodeError
from modules.config import debugEnableTraceback
from utilities import fh_appendMessageBuffer

def handle_operation_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except OperationSuccessful as os:
            funcName = func.__name__
            customMessage = os.args[0] if os.args else ""
            fh_appendMessageBuffer(Color.DEBUG, f'Operation {funcName} finished. {customMessage}')

        except OperationError as oe:
            fh_appendMessageBuffer(Color.DEBUG, str(oe), isLogging=True)

        except OperationCancel as oc:
            fh_appendMessageBuffer(Color.DEBUG, f'{str(oc)}') # need \n cause it breaks on new lines

        except OperationSoftCancel as sc:
            funcName = func.__name__
            customMessage = sc.args[0] if sc.args else ""
            fh_appendMessageBuffer(Color.DEBUG, f'Soft-cancelling {funcName}. {customMessage}')

        except KeyboardInterrupt:
            fh_appendMessageBuffer(Color.DEBUG, 'Keyboard-interrupt detected.')
        
        except JSONDecodeError as jde:
            funcName = func.__name__
            customMessage = f'JSON decoding error in function {funcName}: {jde}'
            fh_appendMessageBuffer(Color.CRITICAL, customMessage, isLogging=True)

        except IOError as ioe:
            funcName = func.__name__
            customMessage = f'{funcName}: {ioe}'
            fh_appendMessageBuffer(Color.CRITICAL, f'Error loading data: {customMessage}', isLogging=True)

        except Exception as e:
            funcName = func.__name__
            customMessage = f'Error in function {funcName}: {e}'
            fh_appendMessageBuffer(Color.CRITICAL, customMessage, isLogging=True)
            # This should forward any exception not handled to our main stack
            if debugEnableTraceback:
                raise Exception()
    return wrapper

# ==============================================
# = Custom Exception for Operation Cancelling. =
# = Will be catched by our main routine.       =
# ==============================================
class OperationCancel(Exception):

    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Operation canceled.'
        super().__init__(self.message)

# ==============================================
# = Custom Exception for Operation Feedback    =
# = Will be catched by our main routine.       =
# ==============================================
class OperationSuccessful(Exception):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Operation succesful.'
        super().__init__(self.message)

# ==============================================
# = Custom Exception for Operation Errors    . =
# = Will be catched by our main routine.       =
# ==============================================
class OperationError(Exception):
    def __init__(self, originalTraceback: Exception = None, message: str = None):
        self.original_exception = originalTraceback
        if message:
            self.message = message
        elif originalTraceback:
            self.message = f'Operation encountered an error: {str(originalTraceback)}'
        else:
            self.message = 'Operation encountered an error.'
        super().__init__(self.message)

# ==============================================================
# = Custom Exception for Propagating messages to main routine. =
# = Will be catched by our main routine.                       =
# ==============================================================
class PropagateResponse(Exception):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = ''
        super().__init__(self.message)

# ======================================================================================
# = Custom Exception for Operation Softcancelling. Doesnt cancel the function raising. =
# = Will be catched by our main routine.                                               =
# ======================================================================================
class OperationSoftCancel(Exception):
    def __init__(self, message=""):
        super().__init__(message)
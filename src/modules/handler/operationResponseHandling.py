# Authors
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: https://github.com/JulianStiebler/
# Date of release: 43.06.2024 
# Last Edited: 24.06.2024

from utilities import cFormatter, Color
import json

def handle_operation_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationSuccessful as os:
            func_name = func.__name__
            custom_message = os.args[0] if os.args else ""
            cFormatter.print(Color.DEBUG, f'Operation {func_name} finished. {custom_message}')
        except OperationError as oe:
            cFormatter.print(Color.DEBUG, str(oe))
        except OperationCancel as oc:
            cFormatter.print(Color.DEBUG, str(oc))
        except json.JSONDecodeError as jde:
            func_name = func.__name__
            error_message = f'JSON decoding error in function {func_name}: {jde}'
            cFormatter.print(Color.CRITICAL, error_message, isLogging=True)
            raise json.JSONDecodeError(error_message)
        except Exception as e:
            func_name = func.__name__
            error_message = f'Error in function {func_name}: {e}'
            cFormatter.print(Color.CRITICAL, error_message, isLogging=True)
            raise OperationError(original_exception=e, message=error_message)
    return wrapper

class OperationCancel(Exception):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Operation canceled.'
        super().__init__(self.message)

class OperationSuccessful(Exception):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Operation succesful.'
        super().__init__(self.message)

class OperationError(Exception):
    def __init__(self, original_exception: Exception = None, message: str = None):
        self.original_exception = original_exception
        if message:
            self.message = message
        elif original_exception:
            self.message = f'Operation encountered an error: {str(original_exception)}'
        else:
            self.message = 'Operation encountered an error.'
        super().__init__(self.message)


class PropagateResponse(Exception):
    def __init__(self, message: str = None):
        if message:
            self.message = message
        else:
            self.message = 'Operation canceled.'
        super().__init__(self.message)

class CustomJSONDecodeError(Exception):
    def __init__(self, message: str = None):
        self.message = message if message else 'JSON decoding error.'
        super().__init__(self.message)
# Authors https://github.com/JulianStiebler/
# Organization: https://github.com/rogueEdit/
# Repository: https://github.com/rogueEdit/OnlineRogueEditor
# Contributors: None except Author
# Date of release: 24.06.2024 
# Last Edited: 28.06.2024

from functools import wraps
from utilities import cFormatter, Color

class HTTPEmptyResponse(Exception):
    def __init__(self, message='Response content is empty.'):
        self.message = message
        super().__init__(self.message)

# Custom status messages for specific HTTP status codes
status_messages = {
    200: (Color.BRIGHT_GREEN, 'Response 200 - That seemed to have worked!'),
    400: (Color.WARNING, 'Response 400 - Bad Request: The server could not understand the request due to invalid syntax. This is usually related to wrong credentials.'),
    401: (Color.BRIGHT_RED, 'Response 401 - Unauthorized: Authentication is required and has failed or has not yet been provided.'),
    403: (Color.BRIGHT_RED, 'Response 403 - Forbidden. We have no authorization to access the resource.'),
    404: (Color.BRIGHT_RED, 'Response 404 - Not Found: The server can not find the requested resource.'),
    405: (Color.BRIGHT_RED, 'Response 405 - Method Not Allowed: The request method is known by the server but is not supported by the target resource.'),
    406: (Color.BRIGHT_RED, 'Response 406 - Not Acceptable: The server cannot produce a response matching the list of acceptable values defined in the request\'s proactive content negotiation headers.'),
    407: (Color.BRIGHT_RED, 'Response 407 - Proxy Authentication Required: The client must first authenticate itself with the proxy.'),
    408: (Color.BRIGHT_RED, 'Response 408 - Request Timeout: The server would like to shut down this unused connection.'),
    413: (Color.BRIGHT_RED, 'Response 413 - Payload Too Large: The request entity is larger than limits defined by server.'),
    429: (Color.BRIGHT_RED, 'Response 429 - Too Many Requests: The user has sent too many requests in a given amount of time ("rate limiting").'),
    500: (Color.CRITICAL, 'Error 500 - Internal Server Error: The server has encountered a situation it does not know how to handle.'),
    502: (Color.CRITICAL, 'Error 502 - Bad Gateway: The server was acting as a gateway or proxy and received an invalid response from the upstream server.'),
    503: (Color.CRITICAL, 'Error 503 - Service Temporarily Unavailable: The server is not ready to handle the request.'),
    504: (Color.CRITICAL, 'Error 504 - Gateway Timeout: The server is acting as a gateway or proxy and did not receive a timely response from the upstream server.'),
    520: (Color.CRITICAL, 'Error 520 - Web Server Returns an Unknown Error: The server has returned an unknown error.'),
    521: (Color.CRITICAL, 'Error 521 - Web Server Is Down: The server is not responding to Cloudflare requests.'),
    522: (Color.CRITICAL, 'Error 522 - Connection Timed Out: Cloudflare was able to complete a TCP connection to the origin server, but the origin server did not reply with an HTTP response.'),
    523: (Color.CRITICAL, 'Error 523 - Origin Is Unreachable: Cloudflare could not reach the origin server.'),
    524: (Color.CRITICAL, 'Error 524 - A Timeout Occurred: Cloudflare was able to complete a TCP connection to the origin server, but the origin server did not reply with an HTTP response.')
}

def handle_http_exceptions(func, requests):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as http_err:
            cFormatter.print(Color.CRITICAL, f'HTTP error occurred: {http_err}')
            if isinstance(args[0], requests.Response) and args[0].status_code in status_messages:
                color, message = status_messages[args[0].status_code]
                cFormatter.print(color, message, isLogging=True)
            else:
                cFormatter.print(Color.CRITICAL, 'Unexpected HTTP error occurred.', isLogging=True)
        except requests.exceptions.RequestException as req_err:
            cFormatter.print(Color.CRITICAL, f'Request error occurred: {req_err}')
        except Exception as e:
            cFormatter.print(Color.CRITICAL, f'Other error occurred: {e}')
    return wrapper

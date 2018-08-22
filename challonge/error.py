class ChallongeError(Exception):

    def __init__(self, message=None, http_body=None, status=None,
                 json_body=None, headers=None):
        super(ChallongeError, self).__init__(message)

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8')
            except BaseException:
                http_body = ('<Could not decode body as utf-8. '
                             'Please report to stephwag@stephwag.com>')

        self.message = message
        self.http_body = http_body
        self.status = status
        self.json_body = json_body
        self.headers = headers or {}

    def __str__(self):
        return self.message or "<empty message>"

class AuthenticationError(ChallongeError):
    pass

class NotFoundError(ChallongeError):
    pass

class InvalidFormatError(ChallongeError):
    pass

class ValidationError(ChallongeError):
    pass

class ServerError(ChallongeError):
    pass
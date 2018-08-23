import json



class ChallongeError(Exception):

    def __init__(self, message=None, http_body=None, status=None,
                 json_body=None, headers=None, request=None):
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
        self.errors = []
        self.request = request

        if self.json_body is not None:
            data = json.loads(self.json_body)
            if 'errors' in data:
                self.errors = data['errors']

    def __str__(self):
        if len(self.errors) > 0:
            msg = ""
            for e in self.errors: msg += e + "\n"
            return msg
        else:
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

def raise_error(r):
    if r.status == 401:
        raise AuthenticationError(status=r.status,message="Unauthorized (Invalid API key or insufficient permissions)",request=r)
    elif r.status == 404:
        raise NotFoundError(status=r.status,message="Object not found within your account scope",request=r)
    elif r.status == 406:
        raise InvalidFormatError(status=r.status,message="Requested format is not supported - request JSON or XML only",request=r)
    elif r.status == 422:
        raise ValidationError(status=r.status,message="Validation error(s) for create or update method",request=r,json_body=r.json())
    else:
        raise ServerError(status=r.status,message="Something went wrong on Challonge's end. If you continually receive this, please contact them.",request=r)

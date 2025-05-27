class ApiError(Exception):

    def __init__(self, code, message='', o_exp=None, payload=None):
        self.code = code
        self.message = message
        self.o_exp = o_exp
        self.payload = payload

    def __str__(self):
        return f'{self.code}:{self.message}'

    def __repr__(self):
        return f'{self.code}:{self.message}'

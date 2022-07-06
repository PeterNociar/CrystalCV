
class BaseException(Exception):
    status_code = 500


class UserAlreadyExists(BaseException):
    status_code = 500
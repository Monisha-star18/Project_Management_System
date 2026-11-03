
from app.exceptions.base_exception import AppException


class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired credentials",
            status_code=401
        )


class InactiveUserError(AppException):
    def __init__(self):
        super().__init__(
            message="User account is inactive",
            status_code=403
        )


class PermissionDeniedError(AppException):
    def __init__(self):
        super().__init__(
            message="You do not have permission to access this service ",
            status_code=403
        )

class InvalidTokenError(AppException):
    def __init__(self):
        super().__init__(
            message="Invalid or expired access token",
            status_code=401
        )
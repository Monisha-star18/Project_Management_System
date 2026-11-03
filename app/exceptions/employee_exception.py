from app.exceptions.base_exception import AppException


class EmployeeAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            message="Employee email or phone already exists",
            status_code=409
        )


class EmployeeNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            message="Employee not found or inactive",
            status_code=404
        )


class InvalidEmployeeUpdateError(AppException):
    def __init__(self):
        super().__init__(
            message="Employee fields cannot be null",
            status_code=422
        )
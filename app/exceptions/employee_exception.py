from app.exceptions.base_exception import AppException


class EmployeeAlreadyExistsError(AppException):

    def __init__(self):
        super().__init__(
            message="Employee email or phone already exists",
            status_code=409
        )

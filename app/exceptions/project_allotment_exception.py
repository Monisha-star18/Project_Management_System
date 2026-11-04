from app.exceptions.base_exception import AppException


class AllotmentNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Project membership not found", status_code=404)


class AllotmentConflictError(AppException):
    def __init__(self, message: str = "Employee is already allotted") -> None:
        super().__init__(message, status_code=409)


class InvalidAllotmentEmployeeError(AppException):
    def __init__(self) -> None:
        super().__init__("Employee must exist and be active", status_code=422)


class ProjectAllotmentNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Project not found", status_code=404)

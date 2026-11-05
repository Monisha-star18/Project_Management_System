
from app.exceptions.base_exception import AppException


class ProjectNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Project not found",
            status_code=404,
        )


class ProjectAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Project name already exists",
            status_code=409,
        )


class InvalidProjectLeadError(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Project lead must be an active team lead",
            status_code=422,
        )


class InvalidProjectUpdateError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=422,
        )

class InvalidProjectDurationError(ValueError):
    def __init__(self):
        super().__init__(
            "Project duration must be at least 7 days"
        )

class ProjectAccessDeniedError(AppException):
    def __init__(self):
        super().__init__(
            message="This team lead does not have permission to access this project's details",
            status_code=403,
        )
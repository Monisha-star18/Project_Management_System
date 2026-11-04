from app.exceptions.base_exception import AppException


class TaskNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__('Task not found', status_code=404)


class TaskAssignmentError(AppException):
    def __init__(self) -> None:
        super().__init__('Employee must have an active project allotment', status_code=422)


class InvalidTaskUpdateError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=422)

from project.core.exceptions.base import BaseWorkHiveException


class IncorrectExceptionUsageError(BaseWorkHiveException):
    def __init__(self, exception: BaseException, message: str | None = None) -> None:
        error_message: str = f'Exception {type(exception)} is used incorrectly'
        if message is not None:
            error_message += f':\n{message}'
        super().__init__(error_message)

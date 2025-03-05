from project.core.exceptions import BaseWorkHiveException


class DotenvNotFoundError(BaseWorkHiveException):
    def __init__(self) -> None:
        super().__init__('Unable to load \".env\" file')


class EnvVarMissingError(BaseWorkHiveException):
    def __init__(self, name: str) -> None:
        super().__init__(f'Evnvironment variable \"{name}\" is missing')


class EnvVarValueError(BaseWorkHiveException):
    def __init__(self, name: str, pattern: str) -> None:
        super().__init__(f'Value of \"{name}\" must match the pattern r\"{pattern}\"')

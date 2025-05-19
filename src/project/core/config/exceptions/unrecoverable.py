from project.core.exceptions import BaseWorkHiveException


class EmptyConfigFileError(BaseWorkHiveException):
    def __init__(self, filename: str) -> None:
        super().__init__(f'Config file \"configs/{filename}.json\" is empty')


class UnknownOptionsError(BaseWorkHiveException):
    def __init__(self, filename: str, unknown_keys: set[str]) -> None:
        error_message: str = ' '.join(
            [
                f'In file \"configs/{filename}.json\"',
                'the following options are not recognized:',
                str(list(unknown_keys)),
            ]
        )
        super().__init__(error_message)


class InvalidOptionTypeError(BaseWorkHiveException):
    def __init__(self, filename: str, option_name: str, correct_type: type) -> None:
        error_message: str = ' '.join(
            [
                f'In file \"configs/{filename}.json\"',
                f'option \"{option_name}\" must be of type \"{correct_type}\"',
            ]
        )
        super().__init__(error_message)

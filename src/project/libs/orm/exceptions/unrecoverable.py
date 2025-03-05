from project.core.exceptions import BaseWorkHiveException


class NotStackableClassError(BaseWorkHiveException):
    def __init__(self, database_path: str, table_name: str, cls: type) -> None:
        error_message: str = ' '.join(
            [
                f'In database \"{database_path}\"',
                f'an error occured upon creating \"{table_name}\" table:',
                f'class \"{cls.__name__}\" is not Stackable',
            ]
        )
        super().__init__(error_message)

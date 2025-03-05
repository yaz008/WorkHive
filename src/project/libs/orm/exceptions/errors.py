from dataclasses import dataclass

from project.core.exceptions import WorkHiveException


@dataclass(slots=True)
class MissingKeyError[Key](WorkHiveException):
    database_path: str
    table_name: str
    key: Key

    def __str__(self) -> str:
        return ', '.join(
            [
                f'In database \"{self.database_path}\"',
                f'in table \"{self.table_name}\"',
                f'key \"{self.key}\" is missing',
            ]
        )

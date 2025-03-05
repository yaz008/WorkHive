from dataclasses import dataclass, field
from datetime import datetime
from json import dumps
from typing import Callable, Any
from uuid import UUID

from project.libs.orm.temp import _TempValue


@dataclass(slots=True)
class SQLiteConverter:
    __hooks: dict[type, Callable[[Any], Any]] = field(default_factory=dict, init=False)
    __sql_type_name: dict[type, str] = field(default_factory=dict, init=False)

    def register_hook[T](
        self,
        type: type[T],
        sqlite_typename: str,
        func: Callable[[T], Any],
    ) -> None:
        self.__hooks |= {type: func}
        self.__sql_type_name |= {type: sqlite_typename}

    def hook[T](self, type: type[T]) -> Callable[[T], Any]:
        return self.__hooks.get(type, lambda v: v)

    def sql_type(self, type: type) -> str:
        return self.__sql_type_name.get(
            type,
            {
                str: 'TEXT',
                bool: 'BOOLEAN',
                int: 'INTEGER',
                float: 'REAL',
                bytes: 'BLOB',
                datetime: 'TIMESTAMP',
            }[type],
        )

    def convert[T](self, value: T) -> Any:
        return self.hook(type=type(value))(value)


sqlite_converter: SQLiteConverter = SQLiteConverter()

sqlite_converter.register_hook(
    type=UUID,
    sqlite_typename='VARCHAR(36)',
    func=lambda uuid: str(uuid),
)
sqlite_converter.register_hook(
    type=_TempValue, sqlite_typename='TEXT', func=lambda value: dumps(value)
)

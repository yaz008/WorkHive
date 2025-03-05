from dataclasses import dataclass, field
from itertools import chain
from sqlite3 import connect, Cursor
from typing import override, Any, get_type_hints, Hashable
from uuid import UUID

from project.configs import DBConfig
from project.libs.orm.exceptions import MissingKeyError, NotStackableClassError
from project.libs.orm.hooks.structure import converter
from project.libs.orm.hooks.unstructure import sqlite_converter
from project.libs.orm.interface import (
    DictLikeTable,
    DictQuery,
    Stackable,
    HasGetOne,
    HasPopOne,
)
from project.libs.orm.tables.sql.query import SingleQuery, MultiQuery


@dataclass
class SQLTable[Key: Hashable, Value, Ret](DictLikeTable[Key, Value, Ret]):
    query: DictQuery = field(init=False)

    def __post_init__(self) -> None:
        self.database = f'{DBConfig.BasePath}\\{self.database}.db'
        with connect(database=self.database) as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(self.query.create)

    @property
    @override
    def keys(self) -> set[Key]:
        with connect(self.database) as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(self.query.select_keys)
            return {
                converter.structure(key[0], self.key_cls) for key in cursor.fetchall()
            }

    @override
    def update(self, __items: dict[Key, Value], /) -> None:
        with connect(self.database, autocommit=True) as connection:
            cursor: Cursor = connection.cursor()
            for key, value in __items.items():
                cursor.execute(
                    self.query.update,
                    tuple(
                        map(
                            sqlite_converter.convert,
                            chain([key], vars(value).values()),
                        )
                    ),
                )


@dataclass
class SingleTable[Key: Hashable, Value](SQLTable[Key, Value, Value]):
    def __post_init__(self):
        self.query = SingleQuery(self.table, self.key_cls, self.value_cls)
        super(SingleTable, self).__post_init__()

    @override
    def __getitem__(self, __key: Key, /) -> Value:
        with connect(self.database) as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(self.query.select, [sqlite_converter.convert(__key)])
        fetched_value: tuple[Any, ...] | None = cursor.fetchone()
        if fetched_value is None:
            raise MissingKeyError(self.database, self.table, __key)
        return converter.structure(
            {
                name: value
                for name, value in zip(
                    get_type_hints(self.value_cls).keys(), fetched_value
                )
            },
            self.value_cls,
        )

    @override
    def remove(self, __key: Key, /) -> None:
        with connect(self.database, autocommit=True) as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(self.query.delete, [sqlite_converter.convert(__key)])


@dataclass
class MultiTable[Key: Hashable, Value: Stackable](
    SQLTable[Key, Value, dict[UUID, Value]],
    HasGetOne[Key, Value],
    HasPopOne[Key, Value],
):
    def __post_init__(self):
        if not issubclass(self.value_cls, Stackable):
            raise NotStackableClassError(self.database, self.table, self.value_cls)
        self.query = MultiQuery(self.table, self.key_cls, self.value_cls)
        super(MultiTable, self).__post_init__()

    @override
    def __getitem__(self, __key: Key, /) -> dict[UUID, Value]:
        with connect(self.database) as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(self.query.select, [sqlite_converter.convert(__key)])
        fetched_values: list[tuple[Any, ...]] = cursor.fetchall()
        return {
            converter.structure(fetched_value[0], UUID): converter.structure(
                {
                    name: value
                    for name, value in zip(
                        get_type_hints(self.value_cls).keys(), fetched_value
                    )
                },
                self.value_cls,
            )
            for fetched_value in fetched_values
        }

    @override
    def remove(self, __key: Key, /) -> None:
        for value in self[__key].values():
            self.remove_one(__key, value.__sql_id__)

    def remove_one(self, __key: Key, __id: UUID, /) -> None:
        with connect(self.database, autocommit=True) as connection:
            cursor: Cursor = connection.cursor()
            cursor.execute(
                self.query.delete,
                [
                    sqlite_converter.convert(__key),
                    sqlite_converter.convert(__id),
                ],
            )

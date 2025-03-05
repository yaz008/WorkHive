from dataclasses import dataclass
from functools import cached_property
from typing import override, get_type_hints, Hashable

from project.libs.orm.hooks.unstructure import sqlite_converter as converter
from project.libs.orm.interface import DictQuery, Stackable


@dataclass(slots=True)
class BaseQuery[Key: Hashable, Value](DictQuery):
    table: str
    key_cls: type[Key]
    value_cls: type[Value]

    @override
    @cached_property
    def select_keys(self) -> str:
        return f'SELECT key FROM {self.table}'

    @override
    @cached_property
    def update(self) -> str:
        colon_names: list[str] = ['key'] + list(get_type_hints(self.value_cls).keys())
        return ' '.join(
            [
                f'INSERT OR REPLACE INTO {self.table}',
                f'({', '.join(colon_names)})',
                f'VALUES ({', '.join(['?'] * len(colon_names))})',
            ]
        )

    @override
    @cached_property
    def select(self) -> str:
        return ' '.join(
            [
                f'SELECT {', '.join(get_type_hints(self.value_cls))}',
                f'FROM {self.table} WHERE key = ?',
            ]
        )


class SingleQuery[Key: Hashable, Value](BaseQuery[Key, Value]):
    @override
    @cached_property
    def create(self) -> str:
        return (
            '\n'.join(
                [
                    f'CREATE TABLE IF NOT EXISTS {self.table}(',
                    f'\tkey {converter.sql_type(self.key_cls)} NOT NULL PRIMARY KEY,\n',
                ]
            )
            + ',\n'.join(
                [
                    f'\t{field_name} {converter.sql_type(field_type)} NOT NULL'
                    for field_name, field_type in get_type_hints(self.value_cls).items()
                ]
            )
            + '\n) WITHOUT ROWID'
        )

    @override
    @cached_property
    def delete(self) -> str:
        return f'DELETE FROM {self.table} WHERE key = ?'


class MultiQuery[Key: Hashable, Value: Stackable](BaseQuery[Key, Value]):
    @override
    @cached_property
    def create(self) -> str:
        return (
            '\n'.join(
                [
                    f'CREATE TABLE IF NOT EXISTS {self.table}(',
                    f'\tkey {converter.sql_type(self.key_cls)} NOT NULL,\n',
                ]
            )
            + ',\n'.join(
                [
                    f'\t{field_name} {converter.sql_type(field_type)} NOT NULL'
                    for field_name, field_type in get_type_hints(self.value_cls).items()
                ]
                + ['\tPRIMARY KEY (key, __sql_id__)']
            )
            + '\n) WITHOUT ROWID'
        )

    @override
    @cached_property
    def delete(self) -> str:
        return f'DELETE FROM {self.table} WHERE key = ? AND __sql_id__ = ?'

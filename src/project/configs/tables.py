from dataclasses import dataclass
from typing import cast

from project.core.config import config


@dataclass(slots=True)
class _DBTable:
    database: str
    table: str


def create_table(dct: dict[str, str]) -> _DBTable:
    return _DBTable(database=dct['database'], table=dct['table'])


@config(
    filename='tables',
    hooks={_DBTable: lambda dct: create_table(dct=cast(dict[str, str], dct))},
)
class TableConfig:
    Sessions: _DBTable = _DBTable(database='with-lifetime', table='sessions')


@config(filename='cache')
class CacheSizeConfig:
    SessionTable: int | None = None

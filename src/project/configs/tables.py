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
    Users: _DBTable = _DBTable(database='userdata', table='users')
    WokhiveID: _DBTable = _DBTable(database='userdata', table='workhive_id')
    Role: _DBTable = _DBTable(database='userdata', table='role')
    State: _DBTable = _DBTable(database='userdata', table='state')
    TempUsers: _DBTable = _DBTable(database='temp-objects', table='users')


@config(filename='cache')
class CacheSizeConfig:
    SessionTable: int | None = None
    UsersTable: int | None = 2**16
    WorkhiveIDTable: int | None = 2**16
    RoleTable: int | None = 2**16
    State: int | None = 2**16
    TempUsersTable: int | None = 1024

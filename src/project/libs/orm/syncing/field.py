from typing import Hashable, overload, cast

from project.libs.orm.interface import DictLikeTable, Stackable
from project.libs.orm.syncing.descriptors import (
    _Synced,
    SingleSyncedValue,
    SingleSyncedField,
    MultiSyncedValue,
)
from project.libs.orm.tables import SingleTable, MultiTable


@overload
def synced[Key: Hashable, Value](
    table: SingleTable[Key, Value], key_field: str
) -> SingleSyncedValue[Key, Value]:
    raise NotImplementedError


@overload
def synced[Key: Hashable, Value](
    table: SingleTable[Key, Value], key_field: str, attrname: str
) -> SingleSyncedField[Key, Value]:
    raise NotImplementedError


@overload
def synced[Key: Hashable, Value: Stackable](
    table: MultiTable[Key, Value], key_field: str
) -> MultiSyncedValue[Key, Value]:
    raise NotImplementedError


def synced[Key: Hashable, Value, Ret](
    table: DictLikeTable[Key, Value, Ret], key_field: str, attrname: str | None = None
) -> _Synced[Key, Value, Ret]:
    if attrname is not None:
        return cast(
            _Synced[Key, Value, Ret], SingleSyncedField(table, key_field, attrname)
        )
    if isinstance(table, MultiTable):
        return cast(_Synced[Key, Value, Ret], MultiSyncedValue(table, key_field))
    return cast(_Synced[Key, Value, Ret], SingleSyncedValue(table, key_field))

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Hashable, override, cast, Any
from uuid import UUID

from project.libs.orm.interface import DictLikeTable, Stackable


@dataclass(slots=True)
class _Synced[Key: Hashable, Value, Ret](ABC):
    _table: DictLikeTable[Key, Value, Ret]
    _key_field: str

    def get_key(self, __obj: object, /) -> Key:
        return cast(Key, getattr(__obj, self._key_field))

    @abstractmethod
    def __get__(self, obj: object, objtype: type | None = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    def __set__(self, obj: object, new: Any) -> None:
        raise NotImplementedError


@dataclass(slots=True)
class _SyncedField[Key: Hashable, Value, Ret](_Synced[Key, Value, Ret]):
    _attrname: str


@dataclass(slots=True)
class SingleSyncedValue[Key: Hashable, Value](_Synced[Key, Value, Value]):
    @override
    def __get__(self, obj: object, _: type | None = None) -> Value:
        return self._table[self.get_key(obj)]

    @override
    def __set__(self, obj: object, new: Value) -> None:
        self._table.update({self.get_key(obj): new})


@dataclass(slots=True)
class SingleSyncedField[Key: Hashable, Value](_SyncedField[Key, Value, Value]):
    @override
    def __get__(self, obj: object, _: type | None = None) -> Any:
        return getattr(self._table[self.get_key(obj)], self._attrname)

    @override
    def __set__(self, obj: object, new: Any) -> None:
        key: Key = getattr(obj, self._key_field)
        table_object: Value = self._table[key]
        setattr(table_object, self._attrname, new)
        self._table.update({key: table_object})


@dataclass(slots=True)
class MultiSyncedValue[Key: Hashable, Value: Stackable](
    _Synced[Key, Value, dict[UUID, Value]]
):
    @override
    def __get__(self, obj: object, _: type | None = None) -> dict[UUID, Value]:
        return self._table[self.get_key(obj)]

    @override
    def __set__(self, obj: object, new: dict[UUID, Value]) -> None:
        self._table.update({self.get_key(obj): v for v in new.values()})

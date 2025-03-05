from abc import ABC
from typing import overload, Hashable
from uuid import UUID

from project.libs.orm.exceptions import MissingKeyError
from project.libs.orm.interface.protocols import (
    HasGetitemProtocol,
    HasKeysProtocol,
    HasUpdateProtocol,
    PopProtocol,
    PopOneProtocol,
    ValuesProtocol,
)
from project.libs.orm.interface.stackable import Stackable


class HasIor[Key: Hashable, Value](ABC):
    def __ior__(
        self: HasUpdateProtocol[Key, Value], __items: dict[Key, Value], /
    ) -> 'HasUpdateProtocol[Key, Value]':
        self.update(__items)
        return self


class HasLen[Key: Hashable](ABC):
    def __len__(self: HasKeysProtocol[Key]) -> int:
        return len(self.keys)


class HasContains[Key: Hashable](ABC):
    def __contains__(self: HasKeysProtocol[Key], __key: Key, /) -> int:
        return __key in self.keys


class HasGet[Key: Hashable, Ret](ABC):
    @overload
    def get(self: HasGetitemProtocol[Key, Ret], __key: Key, /) -> Ret | None:
        raise NotImplementedError

    @overload
    def get(self: HasGetitemProtocol[Key, Ret], __key: Key, __default: Ret, /) -> Ret:
        raise NotImplementedError

    def get(
        self: HasGetitemProtocol[Key, Ret], __key: Key, __default: Ret | None = None, /
    ) -> Ret | None:
        try:
            return self[__key]
        except MissingKeyError:
            return __default


class HasGetOne[Key: Hashable, Value: Stackable](ABC):
    @overload
    def get_one(
        self: HasGetitemProtocol[Key, dict[UUID, Value]], __key: Key, __id: UUID, /
    ) -> Value | None:
        raise NotImplementedError

    @overload
    def get_one(
        self: HasGetitemProtocol[Key, dict[UUID, Value]],
        __key: Key,
        __id: UUID,
        __default: Value,
        /,
    ) -> Value:
        raise NotImplementedError

    def get_one(
        self: HasGetitemProtocol[Key, dict[UUID, Value]],
        __key: Key,
        __id: UUID,
        __default: Value | None = None,
        /,
    ) -> Value | None:
        try:
            return self[__key][__id]
        except MissingKeyError:
            return __default


class HasPop[Key: Hashable, Ret](ABC):
    @overload
    def pop(self: PopProtocol[Key, Ret], __key: Key, /) -> Ret | None:
        raise NotImplementedError

    @overload
    def pop(self: PopProtocol[Key, Ret], __key: Key, __default: Ret, /) -> Ret:
        raise NotImplementedError

    def pop(
        self: PopProtocol[Key, Ret], __key: Key, __default: Ret | None = None, /
    ) -> Ret | None:
        try:
            value = self[__key]
        except MissingKeyError:
            return __default
        self.remove(__key)
        return value


class HasPopOne[Key: Hashable, Value: Stackable](ABC):
    @overload
    def pop_one(
        self: PopOneProtocol[Key, Value], __key: Key, __id: UUID, /
    ) -> Value | None:
        raise NotImplementedError

    @overload
    def pop_one(
        self: PopOneProtocol[Key, Value], __key: Key, __id: UUID, __default: Value, /
    ) -> Value:
        raise NotImplementedError

    def pop_one(
        self: PopOneProtocol[Key, Value],
        __key: Key,
        __id: UUID,
        __default: Value | None = None,
        /,
    ) -> Value | None:
        try:
            value: Value = self[__key][__id]
        except MissingKeyError:
            return __default
        self.remove_one(__key, __id)
        return value


class HasValues[Key: Hashable, Ret](ABC):
    @property
    def values(self: ValuesProtocol[Key, Ret]) -> tuple[Ret, ...]:
        return tuple(self[key] for key in self.keys)


class HasItems[Key: Hashable, Ret](ABC):
    @property
    def items(self: ValuesProtocol[Key, Ret]) -> tuple[tuple[Key, Ret], ...]:
        return tuple((key, self[key]) for key in self.keys)

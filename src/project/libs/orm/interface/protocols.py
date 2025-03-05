from abc import abstractmethod
from typing import Protocol, Hashable
from uuid import UUID

from project.libs.orm.interface.stackable import Stackable


class HasUpdateProtocol[Key: Hashable, Value](Protocol):
    @abstractmethod
    def update(self, __items: dict[Key, Value], /) -> None:
        raise NotImplementedError


class HasGetitemProtocol[Key: Hashable, Ret](Protocol):
    @abstractmethod
    def __getitem__(self, __key: Key, /) -> Ret:
        raise NotImplementedError


class HasRemoveProtocol[Key: Hashable](Protocol):
    @abstractmethod
    def remove(self, __key: Key, /) -> None:
        raise NotImplementedError


class HasRemoveOneProtocol[Key: Hashable](Protocol):
    @abstractmethod
    def remove_one(self, __key: Key, __id: UUID, /) -> None:
        raise NotImplementedError


class PopProtocol[Key: Hashable, Ret](
    HasGetitemProtocol[Key, Ret], HasRemoveProtocol[Key], Protocol
):
    pass


class PopOneProtocol[Key: Hashable, Value: Stackable](
    HasGetitemProtocol[Key, dict[UUID, Value]], HasRemoveOneProtocol[Key], Protocol
):
    pass


class HasKeysProtocol[Key: Hashable](Protocol):
    @property
    @abstractmethod
    def keys(self) -> set[Key]:
        raise NotImplementedError


class ValuesProtocol[Key: Hashable, Ret](
    HasGetitemProtocol[Key, Ret], HasKeysProtocol[Key], Protocol
):
    pass

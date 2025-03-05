from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Hashable

from project.libs.orm.interface.methods import (
    HasIor,
    HasLen,
    HasContains,
    HasGet,
    HasPop,
    HasValues,
    HasItems,
)


class DictLike[Key: Hashable, Value, Ret](
    HasIor[Key, Value],
    HasLen[Key],
    HasContains[Key],
    HasGet[Key, Ret],
    HasPop[Key, Ret],
    HasValues[Key, Ret],
    HasItems[Key, Ret],
):
    @abstractmethod
    def update(self, __items: dict[Key, Value], /) -> None:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, __key: Key, /) -> Ret:
        raise NotImplementedError

    @abstractmethod
    def remove(self, __key: Key, /) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def keys(self) -> set[Key]:
        raise NotImplementedError


@dataclass
class DictLikeTable[Key: Hashable, Value, Ret](DictLike[Key, Value, Ret]):
    database: str
    table: str
    key_cls: type[Key]
    value_cls: type[Value]


class DictQuery(ABC):
    @property
    @abstractmethod
    def create(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def update(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def select(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def delete(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def select_keys(self) -> str:
        raise NotImplementedError

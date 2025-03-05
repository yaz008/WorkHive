from abc import abstractmethod
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Hashable, override

from project.libs.orm.interface import DictLike


@dataclass
class CachedMixin[Key: Hashable, Value, Ret](DictLike[Key, Value, Ret]):
    cache_size: int | None = None
    _cache: OrderedDict[Key, Ret] = field(default_factory=OrderedDict, init=False)
    _cached_keys: set[Key] | None = field(default=None, init=False)

    @abstractmethod
    def _update_cache(self, __different: dict[Key, Value], /) -> None:
        raise NotImplementedError

    @override
    def update(self, __items: dict[Key, Value], /) -> None:
        different: dict[Key, Value] = {
            key: value
            for key, value in __items.items()
            if self._cache.get(key) != value
        }
        self._update_cache(different)
        if self._cached_keys is not None:
            self._cached_keys |= different.keys()
        if self.cache_size is not None:
            while len(self._cache) > self.cache_size:
                self._cache.popitem(last=False)
        super(CachedMixin, self).update(different)  # type: ignore[safe-super]

    @override
    def __getitem__(self, __key: Key, /) -> Ret:
        if __key not in self._cache:
            self._cache |= {
                __key: super(CachedMixin, self).__getitem__(  # type: ignore[safe-super]
                    __key
                )
            }
            if self.cache_size is not None:
                if len(self._cache) > self.cache_size:
                    self._cache.popitem(last=False)
        self._cache.move_to_end(__key)
        return deepcopy(self._cache[__key])

    @override
    @property
    def keys(self) -> set[Key]:
        if self._cached_keys is None:
            self._cached_keys = super(
                CachedMixin, self
            ).keys  # type: ignore[safe-super]
        return self._cached_keys

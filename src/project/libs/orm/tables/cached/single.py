from dataclasses import dataclass
from typing import Hashable, override

from project.libs.orm.tables.cached.mixin import CachedMixin
from project.libs.orm.tables.sql import SingleTable


@dataclass
class CachedSingleTable[Key: Hashable, Value](
    CachedMixin[Key, Value, Value], SingleTable[Key, Value]
):
    @override
    def _update_cache(self, __different: dict[Key, Value], /) -> None:
        self._cache |= __different

    @override
    def remove(self, __key: Key, /) -> None:
        self._cache.pop(__key, None)
        if self._cached_keys is not None:
            self._cached_keys.remove(__key)
        super(CachedSingleTable, self).remove(__key)

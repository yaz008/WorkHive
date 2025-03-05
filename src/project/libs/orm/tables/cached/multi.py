from dataclasses import dataclass
from typing import Hashable, override
from uuid import UUID

from project.libs.orm.interface import Stackable
from project.libs.orm.tables.cached.mixin import CachedMixin
from project.libs.orm.tables.sql import MultiTable


@dataclass
class CachedMultiTable[Key: Hashable, Value: Stackable](
    CachedMixin[Key, Value, dict[UUID, Value]], MultiTable[Key, Value]
):
    @override
    def _update_cache(self, __different: dict[Key, Value], /) -> None:
        for key, value in __different.items():
            if key in self._cache.keys():
                self._cache[key] |= {value.__sql_id__: value}
            else:
                self._cache |= {key: {value.__sql_id__: value}}

    def remove_one(self, __key: Key, __id: UUID, /) -> None:
        item: dict[UUID, Value] = self[__key]
        self._cache[__key].pop(__id, None)
        if len(item) == 1:
            self._cache.pop(__key, None)
        super(CachedMultiTable, self).remove_one(__key, __id)

from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _City:
    city: str


city_table: CachedSingleTable[UUID, _City] = CachedSingleTable(
    database=TableConfig.City.database,
    table=TableConfig.City.table,
    key_cls=UUID,
    value_cls=_City,
    cache_size=TableConfig.City.cache_size,
)

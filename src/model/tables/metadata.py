from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import Stackable, CachedMultiTable


@dataclass
class _Metadata(Stackable):
    value: str


metadata_table: CachedMultiTable[UUID, _Metadata] = CachedMultiTable(
    database=TableConfig.Metadata.database,
    table=TableConfig.Metadata.table,
    key_cls=UUID,
    value_cls=_Metadata,
)

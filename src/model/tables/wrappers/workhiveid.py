from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _WorkHiveIDWrapper:
    value: UUID


workhive_id: CachedSingleTable[int, _WorkHiveIDWrapper] = CachedSingleTable(
    database=TableConfig.WokhiveID.database,
    table=TableConfig.WokhiveID.table,
    key_cls=int,
    value_cls=_WorkHiveIDWrapper,
)

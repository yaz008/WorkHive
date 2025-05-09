from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _TGID:
    value: int


tgid_table: CachedSingleTable[UUID, _TGID] = CachedSingleTable(
    database=TableConfig.TGID.database,
    table=TableConfig.TGID.table,
    key_cls=UUID,
    value_cls=_TGID,
)

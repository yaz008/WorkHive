from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _Balance:
    publications: int
    tokens: int


balance_table: CachedSingleTable[UUID, _Balance] = CachedSingleTable(
    database=TableConfig.Balance.database,
    table=TableConfig.Balance.table,
    key_cls=UUID,
    value_cls=_Balance,
)

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _Datetime:
    value: datetime


datetime_table: CachedSingleTable[UUID, _Datetime] = CachedSingleTable(
    database=TableConfig.Datetime.database,
    table=TableConfig.Datetime.table,
    key_cls=UUID,
    value_cls=_Datetime,
)

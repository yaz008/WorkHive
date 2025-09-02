from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _User:
    language: str
    birth_date: datetime
    full_name: str


user_table: CachedSingleTable[UUID, _User] = CachedSingleTable(
    database=TableConfig.Users.database,
    table=TableConfig.Users.table,
    key_cls=UUID,
    value_cls=_User,
    cache_size=TableConfig.Users.cache_size,
)

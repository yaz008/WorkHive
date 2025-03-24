from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _UserStateWrapper:
    state: str


state_table: CachedSingleTable[UUID, _UserStateWrapper] = CachedSingleTable(
    database=TableConfig.State.database,
    table=TableConfig.State.table,
    key_cls=UUID,
    value_cls=_UserStateWrapper,
)

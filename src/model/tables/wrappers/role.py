from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable


@dataclass
class _UserRoleWrapper:
    role: str


role_table: CachedSingleTable[UUID, _UserRoleWrapper] = CachedSingleTable(
    database=TableConfig.Role.database,
    table=TableConfig.Role.table,
    key_cls=UUID,
    value_cls=_UserRoleWrapper,
)

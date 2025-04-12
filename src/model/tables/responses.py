from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedSingleTable, CachedMultiTable, Stackable


@dataclass
class _Response:
    response_id: UUID
    vacancy_id: UUID
    # point_id: UUID
    owner_id: UUID
    worker_id: UUID
    status: str = 'undefined'


response_map: CachedSingleTable[UUID, _Response] = CachedSingleTable(
    database=TableConfig.ResponseMap.database,
    table=TableConfig.ResponseMap.table,
    key_cls=UUID,
    value_cls=_Response,
)


responses_table: CachedMultiTable[UUID, Stackable] = CachedMultiTable(
    database=TableConfig.Responses.database,
    table=TableConfig.Responses.table,
    key_cls=UUID,
    value_cls=Stackable,
)

from dataclasses import dataclass
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedMultiTable, Stackable


@dataclass
class _Point(Stackable):
    address: str
    name: str
    payload: int
    minimal_charge: int
    charge_per_one: int


points_table: CachedMultiTable[UUID, _Point] = CachedMultiTable(
    database=TableConfig.Points.database,
    table=TableConfig.Points.table,
    key_cls=UUID,
    value_cls=_Point,
)

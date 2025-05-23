from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedMultiTable, Stackable


@dataclass
class _Point(Stackable):
    franchise: str
    address: str
    yandex_link: str
    name: str
    payload: int
    minimal_charge: int
    charge_per_one: int
    creation_time: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.creation_time = datetime.now()


points_table: CachedMultiTable[UUID, _Point] = CachedMultiTable(
    database=TableConfig.Points.database,
    table=TableConfig.Points.table,
    key_cls=UUID,
    value_cls=_Point,
)

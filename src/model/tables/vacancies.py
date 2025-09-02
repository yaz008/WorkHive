from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from project.configs import TableConfig, VacanciesSimpleConfig
from project.libs.orm import CachedMultiTable, Stackable


@dataclass
class _VacancySimple(Stackable):
    point_id: UUID
    owner_id: UUID
    creation_time: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.creation_time = datetime.now()

    @property
    def is_expired(self) -> bool:
        return (
            datetime.now() - self.creation_time > VacanciesSimpleConfig.VacancyLifeTime
        )


simple_vacancies_table: CachedMultiTable[UUID, _VacancySimple] = CachedMultiTable(
    database=TableConfig.VacanciesSimple.database,
    table=TableConfig.VacanciesSimple.table,
    key_cls=UUID,
    value_cls=_VacancySimple,
    cache_size=TableConfig.VacanciesSimple.cache_size,
)

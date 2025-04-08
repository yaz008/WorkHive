from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from project.configs import TableConfig
from project.libs.orm import CachedMultiTable, Stackable


@dataclass
class _VacancySimple(Stackable):
    point_id: UUID
    owner_id: UUID
    expiration_time: datetime


simple_vacancies_table: CachedMultiTable[UUID, _VacancySimple] = CachedMultiTable(
    database=TableConfig.VacanciesSimple.database,
    table=TableConfig.VacanciesSimple.table,
    key_cls=UUID,
    value_cls=_VacancySimple,
)

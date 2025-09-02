from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from model.tables.vacancies import simple_vacancies_table
from project.configs import TableConfig, VacanciesSimpleConfig
from project.libs.orm import CachedSingleTable, CachedMultiTable, Stackable


@dataclass
class _Response:
    response_id: UUID
    vacancy_id: UUID
    # point_id: UUID
    owner_id: UUID
    worker_id: UUID
    worker_telegram_id: int
    status: str = 'undefined'
    is_read_by_owner: bool = False
    is_read_by_worker: bool = False
    creation_time: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.creation_time = datetime.now()

    @property
    def is_expired(self) -> bool:
        return (
            simple_vacancies_table[self.owner_id][self.vacancy_id].creation_time
            + VacanciesSimpleConfig.VacancyLifeTime
            + VacanciesSimpleConfig.ResponseLifeTime
            < datetime.now()
        )


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
    cache_size=TableConfig.Points.cache_size,
)

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from model.tables.vacancies import _VacancySimple
from project.configs import SearchConfig


@dataclass(slots=True)
class _SearchResult:
    vacancies: tuple[_VacancySimple, ...]
    current_index: int | None = None
    __search_time: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.__search_time = datetime.now()

    @property
    def is_expired(self) -> bool:
        return (datetime.now() - self.__search_time) > SearchConfig.LifeTime


search_results_table: dict[UUID, _SearchResult] = dict()

from datetime import timedelta
from typing import cast

from project.core.config import config


@config(
    filename='vacancies-simple',
    hooks={timedelta: lambda hours: timedelta(hours=cast(int, hours))},
)
class VacanciesSimpleConfig:
    VacancyLifeTime: timedelta = timedelta(days=3)
    ResponseLifeTime: timedelta = timedelta(days=1)

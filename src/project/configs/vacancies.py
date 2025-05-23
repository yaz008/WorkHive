from datetime import timedelta
from typing import cast

from project.core.config import config


@config(
    filename='vacancies-simple',
    hooks={timedelta: lambda hours: timedelta(hours=cast(int, hours))},
)
class VacanciesSimpleConfig:
    LifeTime: timedelta = timedelta(days=3)

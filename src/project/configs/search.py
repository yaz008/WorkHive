from datetime import timedelta
from typing import cast

from project.core.config import config


@config(
    filename='search',
    hooks={timedelta: lambda dct: timedelta(minutes=cast(int, dct))},
)
class SearchConfig:
    LifeTime: timedelta = timedelta(minutes=5)

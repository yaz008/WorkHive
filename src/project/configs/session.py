from datetime import timedelta
from typing import cast

from project.core.config import config


@config(
    filename='session',
    hooks={timedelta: lambda minutes: timedelta(minutes=cast(int, minutes))},
)
class SessionConfig:
    ActiveLifeTime: timedelta = timedelta(minutes=10)
    MaxLifeTime: timedelta = timedelta(minutes=16 * 60)

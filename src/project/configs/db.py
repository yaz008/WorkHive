from typing import cast
from uuid import UUID

from project.core.config import config


@config(filename='db', hooks={UUID: lambda string: UUID(cast(str, string))})
class DBConfig:
    BasePath: str = 'database'
    DefaultUUID: UUID = UUID('00000000-0000-0000-0000-000000000000')

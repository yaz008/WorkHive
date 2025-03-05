from dataclasses import dataclass, field
from uuid import UUID, uuid4

from project.configs import DBConfig


@dataclass
class Stackable:
    __sql_id__: UUID = field(default=DBConfig.DefaultUUID, kw_only=True)

    def __post_init__(self):
        if self.__sql_id__ == DBConfig.DefaultUUID:
            self.__sql_id__ = uuid4()

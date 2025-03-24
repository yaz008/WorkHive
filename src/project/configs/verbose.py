from enum import IntEnum
from typing import cast

from project.core.config import config


class VerboseLevel(IntEnum):
    INFO = 0
    WARNING = 1
    ERROR = 2


@config(
    filename='verbose',
    hooks={VerboseLevel: lambda name: getattr(VerboseLevel, cast(str, name))},
)
class VerboseConfig:
    Level: VerboseLevel = VerboseLevel.INFO

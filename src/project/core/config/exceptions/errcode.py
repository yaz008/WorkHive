from dataclasses import dataclass
from enum import StrEnum

from project.core.exceptions import WorkHiveException


class ErrorCode(StrEnum):
    InvalidOptionTypeError = 'InvalidOptionTypeError'


@dataclass
class GetterError(WorkHiveException):
    code: str

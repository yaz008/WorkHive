from dataclasses import dataclass

from project.core.exceptions import WorkHiveException


@dataclass
class UnexpectedStateError(WorkHiveException):
    expected: str
    actual: str

    def __init__(self, expected: str, actual: str) -> None:
        self.expected = expected
        self.actual = actual
        super().__init__(f'Expected \"{self.expected}\", got \"{self.actual}\"')


@dataclass
class InvalidTransitionError(WorkHiveException):
    from_state: str
    symbol: str

    def __post_init__(self) -> None:
        super().__init__(f'(\"{self.from_state}\", \"{self.symbol}\") -> Error')

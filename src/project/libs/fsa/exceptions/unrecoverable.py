from project.configs import FSAState, FSASymbol, FSAConfig
from project.core.exceptions import (
    BaseWorkHiveException,
    IncorrectExceptionUsageError,
)


class InvalidMainDelimiterCountError(BaseWorkHiveException):
    def __init__(self, transition_data: str) -> None:
        match transition_data.count(FSAConfig.MainDelimiter):
            case 0:
                super().__init__(
                    ' '.join(
                        [
                            f'No main delimiter ({FSAConfig.MainDelimiter})',
                            f'in transition_data: \"{transition_data}\"',
                        ]
                    )
                )
            case n if n in (1, 2):
                raise IncorrectExceptionUsageError(
                    exception=self,
                    message='\n'.join(
                        [
                            f'Transition data has valid main delimiter count: {n}',
                            'Acceptable values are: 1, 2',
                        ]
                    ),
                )
            case n if n >= 3:
                super().__init__(
                    ' '.join(
                        [
                            'Too many main delimiters in transition data:',
                            f'expected 1 or 2, got {n}: \"{transition_data}\"',
                        ]
                    )
                )


class DuplicateStateError(BaseWorkHiveException):
    def __init__(self, state: str) -> None:
        super().__init__(f'Duplicate states: \"{state}\"')


class StartNotUniversalError(BaseWorkHiveException):
    def __init__(self) -> None:
        super().__init__(f'Symbol \"{FSASymbol.Start}\" must be universal')


class InitialStateTransitionError(BaseWorkHiveException):
    def __init__(self, state: str, symbol: str) -> None:
        super().__init__(f'(\"{state}\", \"{symbol}\") -> \"{FSAState.Initial}\"')

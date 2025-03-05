from dataclasses import dataclass, field

from project.core.exceptions import WorkHiveException


@dataclass(slots=True)
class LayoutError(WorkHiveException):
    choices_length: int
    layout: tuple[int, ...]

    def __str__(self) -> str:
        return ' '.join(
            [
                f'{self.choices_length} buttons',
                'cannot be structured with layout:',
                str(self.layout),
            ]
        )


@dataclass(slots=True)
class EmptyRowError(WorkHiveException):
    layout: tuple[int, ...]
    zeros: tuple[int, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.zeros = tuple(
            index for index, value in enumerate(self.layout) if value == 0
        )

    def __str__(self) -> str:
        return f'Layout {self.layout} has empty rows at positions {self.zeros}'

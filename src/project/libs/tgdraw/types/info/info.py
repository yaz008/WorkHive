from dataclasses import dataclass, asdict
from typing import cast

from project.libs.tgdraw.types.keyboard import InlineTGButton


@dataclass(slots=True, unsafe_hash=True)
class ButtonInfo:
    text: str
    data: str
    url: str | None = None

    def __iter__(self):
        return iter([self.text, self.data])

    @property
    def asdict(self) -> dict[str, str]:
        return cast(dict[str, str], asdict(self))


@dataclass(slots=True, unsafe_hash=True)
class RowInfo:
    buttons: tuple[ButtonInfo | None, ...]

    def __init__(
        self,
        *buttons: ButtonInfo | None,
    ) -> None:
        self.buttons = buttons

    def render(self) -> tuple[InlineTGButton, ...]:
        return tuple(
            InlineTGButton(**button.asdict)
            for button in self.buttons
            if button is not None
        )


@dataclass(slots=True, unsafe_hash=True)
class LoadInfo:
    name: str
    language: str

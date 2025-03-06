from dataclasses import dataclass, asdict
from itertools import chain
from typing import Callable, cast

from project.configs import ButtonConfig
from project.libs.tgdraw.types.keyboard import InlineTGButton


@dataclass(slots=True, unsafe_hash=True)
class ButtonInfo:
    text: str
    data: str

    def __iter__(self):
        return iter([self.text, self.data])

    @property
    def asdict(self) -> dict[str, str]:
        return cast(dict[str, str], asdict(self))


@dataclass(slots=True, unsafe_hash=True)
class KeyboardInfo:
    buttons: tuple[ButtonInfo, ...]
    layout: tuple[int, ...]
    is_checked: Callable[[int], bool] = lambda _: False

    def render(self) -> tuple[InlineTGButton, ...]:
        return tuple(
            InlineTGButton(
                text=ButtonConfig.CheckDelimiter.join(
                    chain(
                        (ButtonConfig.Checked,) if self.is_checked(index) else (),
                        (button.text,),
                    )
                ),
                data=button.data,
            )
            for index, button in enumerate(self.buttons)
        )


@dataclass(slots=True, unsafe_hash=True)
class LoadInfo:
    name: str
    language: str

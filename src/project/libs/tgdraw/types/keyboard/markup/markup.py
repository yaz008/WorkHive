from dataclasses import dataclass
from itertools import accumulate, chain
from typing import cast

from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from project.libs.tgdraw.exceptions import LayoutError, EmptyRowError
from project.libs.tgdraw.types.keyboard.button import TGButton


@dataclass(slots=True)
class TGKeyboard[Markup: InlineKeyboardMarkup | ReplyKeyboardMarkup]:
    buttons: tuple[TGButton, ...]
    layout: tuple[int, ...]
    cls: type[Markup]

    def __post_init__(self) -> None:
        if len(self.buttons) != sum(self.layout):
            raise LayoutError(len(self.buttons), self.layout)
        if any(row_length == 0 for row_length in self.layout):
            raise EmptyRowError(self.layout)

    @property
    def markup(self) -> Markup:
        return cast(
            Markup,
            self.cls(
                keyboard=[
                    [tgb.button for tgb in self.buttons[start:end]]
                    for start, end in zip(
                        accumulate(chain([0], self.layout[:-1])),
                        accumulate(self.layout),
                    )
                ]
            ),
        )

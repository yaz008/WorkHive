from dataclasses import dataclass
from typing import override

from telebot.types import InlineKeyboardButton

from project.libs.tgdraw.types.keyboard.button.button import TGButton


@dataclass(slots=True)
class InlineTGButton(TGButton):
    data: str
    url: str | None

    @property
    @override
    def button(self) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=self.text, callback_data=self.data)

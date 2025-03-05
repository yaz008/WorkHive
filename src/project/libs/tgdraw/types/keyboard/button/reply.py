from dataclasses import dataclass
from typing import Literal, override

from telebot.types import KeyboardButton

from project.libs.tgdraw.types.keyboard.button.button import TGButton


Request = Literal['request_contact', 'request_location', 'request_poll']


@dataclass(slots=True)
class ReplyTGButton(TGButton):
    request: Request | None = None

    @property
    @override
    def button(self) -> KeyboardButton:
        tgb: KeyboardButton = KeyboardButton(text=self.text)
        if self.request is not None:
            setattr(tgb, self.request, True)
        return tgb

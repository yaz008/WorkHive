from abc import ABC, abstractmethod
from dataclasses import dataclass

from telebot.types import InlineKeyboardButton, KeyboardButton


@dataclass(slots=True)
class TGButton(ABC):
    text: str

    @property
    @abstractmethod
    def button(self) -> InlineKeyboardButton | KeyboardButton:
        raise NotImplementedError

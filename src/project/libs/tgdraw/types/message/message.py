from dataclasses import dataclass
from typing import Literal

from telebot.types import (
    InputMedia,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    LinkPreviewOptions,
)

from project.configs import TGDriverConfig
from project.libs.tgdraw.types.keyboard import TGKeyboard
from project.libs.tgdraw.types.message.media import TGMedia, MediaKind


MessageKind = MediaKind | Literal['Text']


@dataclass(slots=True)
class TGMessage:
    text: str
    tgmedia: TGMedia | None = None
    keyboard: TGKeyboard | None = None
    link_preview: LinkPreviewOptions | None = None

    @property
    def kind(self) -> MessageKind:
        return self.tgmedia.kind if self.tgmedia is not None else 'Text'

    @property
    def media(self) -> InputMedia | None:
        if self.tgmedia is not None:
            return self.tgmedia.type(
                media=self.tgmedia.file_id,
                caption=self.text,
                parse_mode=TGDriverConfig.DefaultParseMode,
            )
        return None

    @property
    def markup(self) -> InlineKeyboardMarkup | ReplyKeyboardMarkup | None:
        return self.keyboard.markup if self.keyboard is not None else None

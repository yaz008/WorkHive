from dataclasses import dataclass
from typing import Literal, cast

from telebot.types import (
    InputMediaAnimation,
    InputMediaDocument,
    InputMediaAudio,
    InputMediaPhoto,
    InputMediaVideo,
    InputMedia,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from project.configs import TGDriverConfig
from project.libs.tgdraw.types.keyboard import TGKeyboard


MessageKind = Literal['Animation', 'Document', 'Audio', 'Photo', 'Video', 'Text']


@dataclass(slots=True)
class TGMedia:
    path: str
    type: InputMedia


@dataclass(slots=True)
class TGMessage:
    text: str
    tgmedia: TGMedia | None = None
    keyboard: TGKeyboard | None = None

    @property
    def kind(self) -> MessageKind:
        return (
            cast(
                dict[InputMedia, MessageKind],
                {
                    InputMediaAnimation: 'Animation',
                    InputMediaDocument: 'Document',
                    InputMediaAudio: 'Audio',
                    InputMediaPhoto: 'Photo',
                    InputMediaVideo: 'Video',
                },
            )[self.tgmedia.type]
            if self.tgmedia is not None
            else 'Text'
        )

    @property
    def media(self) -> InputMedia | None:
        if self.tgmedia is not None:
            with open(file=self.tgmedia.path, mode='rb') as media_file:
                return self.tgmedia.type(
                    media=media_file.read(),
                    caption=self.text,
                    parse_mode=TGDriverConfig.DefaultParseMode,
                )
        else:
            return None

    @property
    def media_bin(self) -> bytes | None:
        if self.tgmedia is not None:
            with open(file=self.tgmedia.path, mode='rb') as media_file:
                return media_file.read()
        else:
            return None

    @property
    def markup(self) -> InlineKeyboardMarkup | ReplyKeyboardMarkup | None:
        return self.keyboard.markup if self.keyboard is not None else None

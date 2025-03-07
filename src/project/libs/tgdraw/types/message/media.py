from dataclasses import dataclass
from typing import cast

from telebot.types import (
    InputMediaAnimation,
    InputMediaDocument,
    InputMediaAudio,
    InputMediaPhoto,
    InputMediaVideo,
    InputMedia,
)

from project.libs.tgdraw.types.message.load import load_media_id, MediaKind


@dataclass(slots=True)
class TGMedia:
    name: str
    kind: MediaKind
    language: str | None = None

    @property
    def file_id(self) -> str:
        return load_media_id(name=self.name, kind=self.kind, language=self.language)

    @property
    def type(self) -> InputMedia:
        return cast(
            dict[MediaKind, InputMedia],
            {
                'Animation': InputMediaAnimation,
                'Document': InputMediaDocument,
                'Audio': InputMediaAudio,
                'Photo': InputMediaPhoto,
                'Video': InputMediaVideo,
            },
        )[self.kind]

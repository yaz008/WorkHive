from json import load
from typing import Literal, cast

from project.configs import MediaConfig, Language
from project.libs.cached import cache


MediaKind = Literal['Animation', 'Document', 'Audio', 'Photo', 'Video']


@cache
def load_media_id(name: str, kind: MediaKind, language: str | None) -> str:
    folder: str = cast(
        dict[MediaKind, str],
        {
            'Animation': MediaConfig.AnimationFolder,
            'Document': MediaConfig.DocumentFolder,
            'Audio': MediaConfig.AudioFolder,
            'Photo': MediaConfig.PhotoFolder,
            'Video': MediaConfig.VideoFolder,
        },
    )[kind]
    with open(
        file=f'{folder}\\{name}.json',
        mode='r',
        encoding='UTF-8',
    ) as button_info:
        return cast(
            str,
            load(button_info)[
                language if language is not None else Language.NoLanguage
            ],
        )

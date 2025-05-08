from dataclasses import dataclass
from typing import Literal, cast

from project.core.config import config
from project.libs.cached import cache


@dataclass(slots=True)
class _Language:
    code: str
    native_name: str


def create_language(dct: dict[str, str]) -> _Language:
    return _Language(code=dct['code'], native_name=dct['native_name'])


@config(
    filename='language',
    hooks={_Language: lambda dct: create_language(dct=cast(dict[str, str], dct))},
)
class Language:
    English: _Language = _Language(code='en', native_name='English')
    Russian: _Language = _Language(code='ru', native_name='Русский')
    Kazakh: _Language = _Language(code='kk', native_name='Қазақ')
    Belarusian: _Language = _Language(code='be', native_name='Беларуская')
    Uzbek: _Language = _Language(code='uz', native_name='Оʻzbek')
    DefaultCode: str = 'ru'
    NoLanguage: str = 'no-language'

    @cache
    @staticmethod
    def attrtuple(attrname: Literal['code', 'native_name']) -> tuple[str, ...]:
        return tuple(
            getattr(getattr(Language, lang), attrname)
            for lang in Language.__annotations__.keys()
            if lang not in ('DefaultCode', 'NoLanguage')
        )

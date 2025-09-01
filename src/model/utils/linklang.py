from re import sub
from typing import Final


YANDEX_LANGUAGE_CODE: Final[dict[str, str]] = {
    'be': 'be_BY',
    'en': 'en_US',
    'hy': 'hy_AM',
    'kk': 'kk_KZ',
    'ky': 'ky_KG',
    'ru': 'ru_RU',
    'uz': 'uz_UZ',
}


YANDEX_LANGUAGE_DOMAIN: Final[dict[str, str]] = {
    'be': 'by',
    'en': 'com',
    'hy': 'am',
    'kk': 'kz',
    'ky': 'kg',
    'ru': 'ru',
    'uz': 'uz',
}


def parse_link_params(params: str) -> dict[str, str]:
    return {
        p[0]: p[1]
        for p in map(
            lambda p: p.split(sep='=', maxsplit=1),
            params.split(sep='&'),
        )
    }


def with_yandex_language(link: str, language_code: str) -> str:
    base, *unparsed_params = link.split(sep='?', maxsplit=1)
    params: dict[str, str] = (
        parse_link_params(unparsed_params[0]) if len(unparsed_params) != 0 else dict()
    ) | {'lang': YANDEX_LANGUAGE_CODE[language_code]}
    return f'{(
        sub(
            fr'https://yandex\.[a-z]+/',
            fr'https://yandex.{YANDEX_LANGUAGE_DOMAIN[language_code]}/',
            string=base,
        )
    )}?{'&'.join(f'{k}={v}' for k, v in params.items())}'

from functools import partial
from json import loads
from pathlib import Path
from typing import Final

from Levenshtein import distance

from model.tables import _Metadata, metadata_table
from model.types import User


def in_metadata(user: User, value: str) -> bool:
    return value in [m.value for m in user.metadata.values()]


def add_metadata(user: User, value: str) -> None:
    metadata_table.update({user.workhive_id: _Metadata(value=value)})


CITIES_IN_RUSSIA_TXT: Final[Path] = Path('assets/data/cities-in-russia.json')
CITIES_IN_RUSSIA: Final[dict[str, str]] = {
    city.lower(): city
    for city in loads(CITIES_IN_RUSSIA_TXT.read_text(encoding='utf-8'))
}


def find_closest(city: str) -> str:
    city_lower: str = city.lower()
    return CITIES_IN_RUSSIA[
        (
            min(
                CITIES_IN_RUSSIA,
                key=partial(
                    distance,
                    city_lower.replace(' ', '-'),
                    weights=(6, 6, 5),
                    score_hint=1,
                ),
            )
            if city_lower not in CITIES_IN_RUSSIA
            else city_lower
        )
    ]

from dataclasses import dataclass
from datetime import datetime
from typing import cast

from project.core.config import config, JSON


@dataclass(slots=True)
class Promocode:
    vacancies: int
    tokens: int
    expiration_date: datetime

    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.expiration_date


class PromocodeDictType(dict[str, Promocode]):
    pass


def load_promocode(dct: dict[str, JSON]) -> Promocode:
    return Promocode(
        vacancies=cast(int, dct.get('Vacancies', 0)),
        tokens=cast(int, dct.get('Tokens', 0)),
        expiration_date=(
            datetime.strptime(cast(str, dct['ExpirationDate']), '%d.%m.%Y')
            if 'ExpirationDate' in dct
            else datetime.now()
        ),
    )


@config(
    filename='promocodes',
    hooks={
        PromocodeDictType: lambda dct: {
            promocode: load_promocode(cast(dict[str, JSON], promocode_dct))
            for promocode, promocode_dct in cast(dict[str, JSON], dct).items()
        }
    },
)
class PromocodeConfig:
    Promocodes: PromocodeDictType = PromocodeDictType()

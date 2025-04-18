# mypy: disable-error-code="assignment"
from typing import Any

from model.tables import temp_points
from model.types.temp._descriptor import TempDescriptor
from project.libs.orm import synced


class TempPoint:
    telegram_id: int
    franchise: str = TempDescriptor('franchise')
    address: str = TempDescriptor('address')
    yandex_link: str = TempDescriptor('yandex_link')
    name: str = TempDescriptor('name')
    payload: int = TempDescriptor('payload')
    minimal_charge: int = TempDescriptor('minimal_charge')
    charge_per_one: int = TempDescriptor('charge_per_one')
    dct: dict[str, Any] = synced(temp_points, 'telegram_id', 'value')

    def __init__(self, telegram_id: int, /, set_default: bool = False) -> None:
        self.telegram_id = telegram_id
        if set_default:
            self.franchise = str()
            self.address = str()
            self.yandex_link = str()
            self.name = str()
            self.payload = 0
            self.minimal_charge = 0
            self.charge_per_one = 0

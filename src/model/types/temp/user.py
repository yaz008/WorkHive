# mypy: disable-error-code="assignment"
from typing import Any

from model.tables import temp_users
from model.types.temp._descriptor import TempDescriptor
from project.configs import FSAState, Language
from project.libs.orm import synced


class TempUser:
    telegram_id: int
    state: str = TempDescriptor('state')
    language: str = TempDescriptor('language')
    role: str = TempDescriptor('role')
    full_name: str = TempDescriptor('full_name')
    birth_date: str = TempDescriptor('birth_date')
    concent_pp: bool = TempDescriptor('concent_pp')
    concent_ad: bool = TempDescriptor('concent_pd')
    concent_of: bool = TempDescriptor('concent_oa')
    dct: dict[str, Any] = synced(temp_users, 'telegram_id', 'value')

    def __init__(self, telegram_id: int, set_default: bool = False) -> None:
        self.telegram_id = telegram_id
        if set_default:
            self.state = FSAState.Initial
            self.language = Language.DefaultCode
            self.role = str()
            self.full_name = str()
            self.birth_date = str()
            self.concent_pp = False
            self.concent_ad = False
            self.concent_of = False

# mypy: disable-error-code="assignment"
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from model.tables import (
    user_table,
    state_table,
    role_table,
    workhive_id,
    _UserRoleWrapper,
    _UserStateWrapper,
    _WorkHiveIDWrapper,
    _User,
)
from model.types.temp import TempUser
from project.libs.orm import synced


@dataclass
class User:
    telegram_id: int
    state: str = synced(state_table, 'workhive_id', 'state')
    language: str = synced(user_table, 'workhive_id', 'language')
    role: str = synced(role_table, 'workhive_id', 'role')
    full_name: str = synced(user_table, 'workhive_id', 'full_name')
    birth_date: str = synced(user_table, 'workhive_id', 'birth_date')

    @property
    def workhive_id(self) -> UUID:
        return workhive_id[self.telegram_id].value

    def __init__(self, telegram_id: int) -> None:
        self.telegram_id = telegram_id


def to_datetime(birth_date: str) -> datetime:
    day, month, year = birth_date[0:2], birth_date[2:4], birth_date[4:8]
    try:
        return datetime(year=int(year), month=int(month), day=int(day))
    except ValueError:
        return datetime(year=1, month=1, day=1)


def create_user(temp_user: TempUser) -> User:
    user: User = User(telegram_id=temp_user.telegram_id)
    workhive_id.update({temp_user.telegram_id: _WorkHiveIDWrapper(value=uuid4())})
    state_table.update({user.workhive_id: _UserStateWrapper(state=temp_user.state)})
    role_table.update({user.workhive_id: _UserRoleWrapper(role=temp_user.role)})
    user_table.update(
        {
            user.workhive_id: _User(
                language=temp_user.language,
                birth_date=to_datetime(temp_user.birth_date),
                full_name=temp_user.full_name,
            )
        }
    )
    return user

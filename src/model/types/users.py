# mypy: disable-error-code="assignment"
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from model.tables import (
    user_table,
    state_table,
    role_table,
    workhive_id,
    points_table,
    simple_vacancies_table,
    balance_table,
    metadata_table,
    tgid_table,
    datetime_table,
    _UserRoleWrapper,
    _UserStateWrapper,
    _WorkHiveIDWrapper,
    _User,
    _Point,
    _VacancySimple,
    _Balance,
    _Metadata,
    _TGID,
    _Datetime,
)
from model.types.temp import TempUser
from project.libs.orm import synced


class User:
    telegram_id: int
    metadata: dict[UUID, _Metadata] = synced(metadata_table, 'workhive_id')
    state: str = synced(state_table, 'workhive_id', 'state')
    language: str = synced(user_table, 'workhive_id', 'language')
    role: str = synced(role_table, 'workhive_id', 'role')
    full_name: str = synced(user_table, 'workhive_id', 'full_name')
    birth_date: str = synced(user_table, 'workhive_id', 'birth_date')
    registration_datetime: datetime = synced(datetime_table, 'workhive_id', 'value')

    @property
    def workhive_id(self) -> UUID:
        return workhive_id[self.telegram_id].value


def to_datetime(birth_date: str) -> datetime:
    day, month, year = birth_date[0:2], birth_date[2:4], birth_date[4:8]
    try:
        return datetime(year=int(year), month=int(month), day=int(day))
    except ValueError:
        return datetime(year=1, month=1, day=1)


@dataclass
class Owner(User):
    points: dict[UUID, _Point] = synced(points_table, 'workhive_id')
    simple_vacancies: dict[UUID, _VacancySimple] = synced(
        simple_vacancies_table, 'workhive_id'
    )
    balance: _Balance = synced(balance_table, 'workhive_id')

    def __init__(self, telegram_id: int) -> None:
        self.telegram_id = telegram_id


@dataclass
class Worker(User):
    def __init__(self, telegram_id: int) -> None:
        self.telegram_id = telegram_id


def create_user(temp_user: TempUser) -> Worker | Owner:
    id: UUID = uuid4()
    tgid_table.update({id: _TGID(value=temp_user.telegram_id)})
    workhive_id.update({temp_user.telegram_id: _WorkHiveIDWrapper(value=id)})
    state_table.update({id: _UserStateWrapper(state=temp_user.state)})
    role_table.update({id: _UserRoleWrapper(role=temp_user.role)})
    datetime_table.update({id: _Datetime(value=datetime.now())})
    user_table.update(
        {
            id: _User(
                language=temp_user.language,
                birth_date=(
                    to_datetime(temp_user.birth_date)
                    if temp_user.role == 'worker'
                    else datetime.now()
                ),
                full_name=temp_user.full_name,
            )
        }
    )
    match temp_user.role:
        case 'worker':
            return Worker(telegram_id=temp_user.telegram_id)
        case 'owner':
            balance_table.update({id: _Balance(publications=0, tokens=0)})
            return Owner(telegram_id=temp_user.telegram_id)
    raise

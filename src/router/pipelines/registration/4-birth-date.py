from datetime import datetime, timedelta
from re import match

from model.types import TempUser, to_datetime
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, numeric
from project.libs.tght import render_file
from router.instance import router


def render_birth_date(placeholder: str, birth_date: str) -> str:
    result: str = placeholder
    for digit in birth_date:
        result = result.replace('_', digit, count=1)
    return result


def is_birth_date_valid(birth_date: datetime | None) -> bool:
    if birth_date is None:
        return False
    age: timedelta = datetime.now() - birth_date
    return timedelta(14 * 365 + 3) < age < timedelta(120 * 365 + 30)


@router.add(
    name=FSAState.BirthDate,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.FullName,
        FSASymbol.Next: FSAState.PrivacyPolicyConsent,
        FSASymbol.InputData: FSAState.BirthDate,
        FSASymbol.Error: FSAState.BirthDateErr,
    },
    accepts_types=('text',),
)
def birth_date(user: TempUser, factory: ButtonFactoryClosure, digit: str) -> TGMessage:
    match digit:
        case d if (d in '0123456789') and len(d) == 1 and len(user.birth_date) < 8:
            user.birth_date += d
        case d if match(pattern=r'^\d\d\.\d\d\.\d\d\d\d$', string=d) is not None:
            user.birth_date = d.replace('.', str())
        case '<' if len(user.birth_date) > 0:
            user.birth_date = user.birth_date[:-1]
        case d if d != str():
            user.birth_date = str()
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
            tag_handlers={
                'birth-date': lambda placeholder: render_birth_date(
                    placeholder, user.birth_date
                )
            },
        ),
        keyboard=numeric(
            factory=factory,
            symbol=FSASymbol.InputData,
            back=factory.saved(WorkHiveButton.Back),
            next=(
                (
                    factory.saved(WorkHiveButton.Next, args=(user.concent_pp,))
                    if is_birth_date_valid(birth_date=to_datetime(user.birth_date))
                    else factory.saved(WorkHiveButton.NextErr)
                )
                if len(user.birth_date) == 8
                else None
            ),
        ),
    )

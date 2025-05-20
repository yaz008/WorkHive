from re import match

from model.types import TempUser, to_datetime
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, RowInfo, ButtonFactoryClosure, keyboard
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.registration.utils import render_birth_date, is_birth_date_valid


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
                'role': lambda placeholder: (
                    f'<code>{user.role if user.role != str() else placeholder}</code>'
                ),
                'full-name': lambda placeholder: (
                    f'<code>{user.full_name}</code>'
                    if user.full_name != str()
                    else f'<code>{placeholder}</code>'
                ),
                'birth-date': lambda placeholder: f'<code>{render_birth_date(
                    placeholder, user.birth_date
                )}</code>',
                'consent-pp': lambda _: '✅' if user.concent_pp else '❌',
                'consent-ad': lambda _: '✅' if user.concent_ad else '❌',
                'consent-of': lambda _: '✅' if user.concent_of else '❌',
            },
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(WorkHiveButton.Back),
                (
                    (
                        factory.saved(WorkHiveButton.Next, args=(user.concent_pp,))
                        if is_birth_date_valid(birth_date=to_datetime(user.birth_date))
                        else factory.saved(WorkHiveButton.NextErr)
                    )
                    if len(user.birth_date) == 8
                    else None
                ),
            ),
        ),
    )

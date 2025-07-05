from typing import cast

from model.types import TempUser
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, choice
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.registration.utils import render_birth_date


@router.add(
    name=FSAState.ChooseRole,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.ChooseLanguage,
        FSASymbol.InputData: FSAState.ChooseRole,
        FSASymbol.Next: FSAState.Register,
    },
)
def choose_role(user: TempUser, factory: ButtonFactoryClosure, role: str) -> TGMessage:
    user.role = role
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
        keyboard=choice(
            (
                factory.saved(WorkHiveButton.Worker, args=('worker',)),
                factory.saved(WorkHiveButton.Owner, args=('owner',)),
            ),
            cast(
                dict[str, int],
                {
                    'worker': 0,
                    'owner': 1,
                },
            ).get(user.role),
            RowInfo(
                factory.saved(WorkHiveButton.Back, args=(user.language,)),
                (
                    factory.saved(WorkHiveButton.Next)
                    if user.role in ('worker', 'owner')
                    else None
                ),
            ),
        ),
    )

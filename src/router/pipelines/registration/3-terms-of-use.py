from model.types import TempUser
from project.configs import (
    FSAState,
    FSASymbol,
    FSAPipeline,
    WorkHiveButton,
)
from project.libs.tgdraw import (
    TGMessage,
    ButtonFactoryClosure,
    RowInfo,
    choice,
)
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.registration.utils import render_birth_date


@router.add(
    name=FSAState.TermsOfUseConsent,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.Register,
        FSASymbol.Next: FSAState.OwnerMainMenu,
        FSASymbol.Error: FSAState.WorkerMainMenu,
        FSASymbol.InputData: FSAState.TermsOfUseConsent,
    },
)
def terms_of_use_concent(
    user: TempUser, factory: ButtonFactoryClosure, concent: bool
) -> TGMessage:
    user.concent_of = concent
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
            (factory.saved(WorkHiveButton.Consent, args=(not user.concent_of,)),),
            0 if user.concent_of else None,
            RowInfo(
                factory.saved(WorkHiveButton.Back),
                (
                    factory.saved(
                        WorkHiveButton.Next
                        if user.role == 'owner'
                        else WorkHiveButton.NextErr
                    )
                    if user.concent_of
                    else None
                ),
            ),
        ),
    )

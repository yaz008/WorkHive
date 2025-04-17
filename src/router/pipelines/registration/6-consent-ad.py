from model.types import TempUser
from project.configs import (
    FSAState,
    FSASymbol,
    FSAPipeline,
    WorkHiveButton,
    WorkHiveDocument,
)
from project.libs.tgdraw import (
    TGMessage,
    ButtonFactoryClosure,
    TGMedia,
    RowInfo,
    choice,
)
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.registration.utils import render_birth_date


@router.add(
    name=FSAState.AdvertisingConsent,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.PrivacyPolicyConsent,
        FSASymbol.Next: FSAState.OfferConsent,
        FSASymbol.InputData: FSAState.AdvertisingConsent,
    },
)
def privacy_policy_concent(
    user: TempUser, factory: ButtonFactoryClosure, concent: bool
) -> TGMessage:
    user.concent_ad = concent
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
        tgmedia=TGMedia(
            name=WorkHiveDocument.AdvertisingConsent,
            kind='Document',
            language=user.language,
        ),
        keyboard=choice(
            (factory.saved(WorkHiveButton.Consent, args=(not user.concent_ad,)),),
            0 if user.concent_ad else None,
            RowInfo(
                factory.saved(WorkHiveButton.Back, args=(user.concent_pp,)),
                (
                    factory.saved(WorkHiveButton.Next, args=(user.concent_of,))
                    if user.concent_ad
                    else None
                ),
            ),
        ),
    )

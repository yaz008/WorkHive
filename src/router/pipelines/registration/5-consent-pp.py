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


@router.add(
    name=FSAState.PrivacyPolicyConsent,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.BirthDate,
        FSASymbol.Next: FSAState.AdvertisingConsent,
        FSASymbol.InputData: FSAState.PrivacyPolicyConsent,
    },
)
def privacy_policy_concent(
    user: TempUser, factory: ButtonFactoryClosure, concent: bool
) -> TGMessage:
    user.concent_pp = concent
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        tgmedia=TGMedia(
            name=WorkHiveDocument.PrivacyPolicy,
            kind='Document',
            language=user.language,
        ),
        keyboard=choice(
            (factory.saved(WorkHiveButton.Consent, args=(not user.concent_pp,)),),
            0 if user.concent_pp else None,
            RowInfo(
                factory.saved(WorkHiveButton.Back),
                (
                    factory.saved(WorkHiveButton.Next, args=(user.concent_ad,))
                    if user.concent_pp
                    else None
                ),
            ),
        ),
    )

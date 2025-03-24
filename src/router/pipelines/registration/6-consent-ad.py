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

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
    name=FSAState.OfferConsent,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.AdvertisingConsent,
        FSASymbol.Next: FSAState.OwnerMainMenu,
        FSASymbol.Error: FSAState.WorkerMainMenu,
        FSASymbol.InputData: FSAState.OfferConsent,
    },
)
def privacy_policy_concent(
    user: TempUser, factory: ButtonFactoryClosure, concent: bool
) -> TGMessage:
    user.concent_of = concent
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        tgmedia=TGMedia(
            name=WorkHiveDocument.Offer,
            kind='Document',
            language=user.language,
        ),
        keyboard=choice(
            (factory.saved(WorkHiveButton.Consent, args=(not user.concent_of,)),),
            0 if user.concent_of else None,
            RowInfo(
                factory.saved(WorkHiveButton.Back, args=(user.concent_ad,)),
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

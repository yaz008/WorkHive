from model.types import User
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerNoADConsent,
    pipeline=FSAPipeline.OwnerNoADConsent,
    transitions={
        FSASymbol.InputData: FSAState.OwnerMainMenu,
    },
)
def owner_no_ad_consent(user: User, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Consent)),
        ),
    )

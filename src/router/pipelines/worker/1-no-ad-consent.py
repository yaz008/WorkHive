from model.types import User
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.WorkerNoADConsent,
    pipeline=FSAPipeline.WorkerNoADConsent,
    transitions={
        FSASymbol.InputData: FSAState.WorkerMainMenu,
    },
)
def worker_no_ad_consent(user: User, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Consent)),
        ),
    )

from model.types import User
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.WorkerRevokeConsentConfirm,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.Confirm: FSAState.WorkerNoADConsent,
        FSASymbol.Back: FSAState.WorkerSettings,
    },
)
def worker_revoke_consent(user: User, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.YesIAmSure)),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

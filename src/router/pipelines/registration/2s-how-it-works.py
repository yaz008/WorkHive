from model.types import TempUser
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.HowItWorks,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.Register,
        FSASymbol.Next: FSAState.TermsOfUseConsent,
    },
)
def register(user: TempUser, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=user.language,
            state=f'{user.state}-for-{user.role}s',
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Register)),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

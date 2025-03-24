from model.types import TempUser
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.Register,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.ChooseLanguage,
        FSASymbol.Next: FSAState.ChooseRole,
    },
)
def register(user: TempUser, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Register, args=(user.role,))),
            RowInfo(factory.saved(WorkHiveButton.Back, args=(user.language,))),
        ),
    )

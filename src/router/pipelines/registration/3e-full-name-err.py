from model.types import TempUser
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.FullNameErr,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.FullName,
    },
)
def full_name_err(user: TempUser, factory: ButtonFactoryClosure) -> TGMessage:
    user.full_name = str()
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

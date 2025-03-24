from typing import cast

from model.types import TempUser
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, choice
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.ChooseRole,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.Register,
        FSASymbol.InputData: FSAState.ChooseRole,
        FSASymbol.Next: FSAState.FullName,
    },
)
def choose_role(user: TempUser, factory: ButtonFactoryClosure, role: str) -> TGMessage:
    user.role = role
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=choice(
            (
                factory.saved(WorkHiveButton.Worker, args=('worker',)),
                factory.saved(WorkHiveButton.Owner, args=('owner',)),
            ),
            cast(
                dict[str, int],
                {
                    'worker': 0,
                    'owner': 1,
                },
            ).get(user.role),
            RowInfo(
                factory.saved(WorkHiveButton.Back),
                (
                    factory.saved(WorkHiveButton.Next)
                    if user.role in ('worker', 'owner')
                    else None
                ),
            ),
        ),
    )

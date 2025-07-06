from model.types import TempUser
from project.configs import (
    FSAState,
    FSASymbol,
    FSAPipeline,
    WorkHiveButton,
    ChennelConfig,
)
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.Register,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.ChooseRole,
        FSASymbol.HowItWorks: FSAState.HowItWorks,
        FSASymbol.Next: FSAState.FullName,
    },
)
def register(user: TempUser, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=user.language,
            state=f'{user.state}-{user.role}',
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Register)),
            RowInfo(factory.saved(WorkHiveButton.HowItWorks)),
            RowInfo(
                factory.saved(
                    WorkHiveButton.SubscribeToOurChannel,
                    url=(
                        ChennelConfig.OwnersChannelLink
                        if user.role == 'owner'
                        else ChennelConfig.WorkersChannelLink
                    ),
                )
            ),
            RowInfo(factory.saved(WorkHiveButton.Back, args=(user.role,))),
        ),
    )

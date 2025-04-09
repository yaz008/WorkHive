from model.tables import temp_users
from model.types import User, TempUser, create_user
from project.configs import FSASymbol, FSAState, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.WorkerMainMenu,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.Settings: FSAState.WorkerSettings,
        FSASymbol.Search: FSAState.WorkerSearchResults,
        FSASymbol.Responds: FSAState.WorkerResponds,
    },
)
def register(user: User | TempUser, factory: ButtonFactoryClosure) -> TGMessage:
    if isinstance(user, TempUser):
        user = create_user(user)
        temp_users.remove(user.telegram_id)
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Search)),
            RowInfo(factory.saved(WorkHiveButton.MyResponds)),
            RowInfo(factory.saved(WorkHiveButton.Settings)),
        ),
    )

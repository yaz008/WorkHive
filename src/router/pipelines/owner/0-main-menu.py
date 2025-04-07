from model.tables import temp_users
from model.types import User, TempUser, create_user
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerMainMenu,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Publish: FSAState.OwnerPublish,
        FSASymbol.Points: FSAState.OwnerPoints,
        FSASymbol.Vacancies: FSAState.OwnerVacancies,
        FSASymbol.Notifications: FSAState.OwnerNotifications,
        FSASymbol.Settings: FSAState.OwnerSettings,
        FSASymbol.Subscription: FSAState.OwnerSubstription,
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
            RowInfo(
                factory.saved(WorkHiveButton.Publish),
                factory.saved(WorkHiveButton.MyPoints),
                factory.saved(WorkHiveButton.MyVacancies),
            ),
            RowInfo(factory.saved(WorkHiveButton.Notifications)),
            RowInfo(
                factory.saved(WorkHiveButton.Settings),
                factory.saved(WorkHiveButton.Subsrciption),
            ),
        ),
    )

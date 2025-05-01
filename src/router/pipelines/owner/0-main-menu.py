from typing import cast

from model.tables import (
    _Response,
    temp_users,
    response_map,
    responses_table,
)
from model.types import Owner, TempUser, create_user
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


def get_notifications(owner: Owner) -> list[_Response]:
    return [
        response_map[response.__sql_id__]
        for response in responses_table[owner.workhive_id].values()
        if response_map[response.__sql_id__].status == 'undefined'
    ]


@router.add(
    name=FSAState.OwnerMainMenu,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Points: FSAState.OwnerPoints,
        FSASymbol.Vacancies: FSAState.OwnerVacancies,
        FSASymbol.Notifications: FSAState.OwnerNotifications,
        FSASymbol.Settings: FSAState.OwnerSettings,
        FSASymbol.Subscription: FSAState.OwnerSubstription,
    },
)
def register(owner: Owner | TempUser, factory: ButtonFactoryClosure) -> TGMessage:
    if isinstance(owner, TempUser):
        owner = cast(Owner, create_user(owner))
        temp_users.remove(owner.telegram_id)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(WorkHiveButton.MyPoints),
                factory.saved(WorkHiveButton.MyVacancies),
            ),
            RowInfo(
                factory.saved(
                    (
                        WorkHiveButton.NotificationsNew
                        if any(
                            not notification.is_read_by_owner
                            for notification in get_notifications(owner)
                        )
                        else WorkHiveButton.Notifications
                    ),
                    args=(str(), '0'),
                )
            ),
            RowInfo(
                factory.saved(WorkHiveButton.Settings),
                factory.saved(WorkHiveButton.Subsrciption),
            ),
        ),
    )

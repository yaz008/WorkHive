from model.tables import (
    _Response,
    response_map,
    responses_table,
    user_table,
    simple_vacancies_table,
    points_table,
)
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


def delete_response(owner: Owner, index: str) -> None:
    if index != str():
        response: _Response = [
            response_map[id.__sql_id__]
            for id in responses_table[owner.workhive_id].values()
        ][int(index)]
        responses_table.remove_one(response.owner_id, response.response_id)
        responses_table.remove_one(response.vacancy_id, response.response_id)
        # responses_table.remove_one(response.point_id, response.response_id)
        responses_table.remove_one(response.worker_id, response.response_id)
        response_map.remove(response.response_id)


@router.add(
    name=FSAState.OwnerNotifications,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Accept: FSAState.OwnerNotifications,
        FSASymbol.Decline: FSAState.OwnerNotifications,
        FSASymbol.Next: FSAState.OwnerNotifications,
        FSASymbol.Back: FSAState.OwnerNotifications,
        FSASymbol.Ok: FSAState.OwnerMainMenu,
    },
)
def owner_settings(
    owner: Owner, factory: ButtonFactoryClosure, action: str, index: str
) -> TGMessage:
    notifications: list[_Response] = [
        response_map[response.__sql_id__]
        for response in responses_table[owner.workhive_id].values()
        if response_map[response.__sql_id__].status == 'undefined'
    ]
    if index != str():
        index = '0'
    notification: _Response = notifications[int(index)]
    match action:
        case 'accept':
            response_map[notification.response_id].status = 'accepted'
            delete_response(owner, index)
        case 'decline':
            response_map[notification.response_id].status = 'declined'
            delete_response(owner, index)
        case 'next':
            index = str(int(index) + 1)
        case 'back':
            index = str(int(index) - 1)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=(
                owner.state if len(notifications) > 0 else FSAState.OwnerNoNotifications
            ),
            tag_handlers={
                'telegram-tag': lambda _: '@no_tag_provided',
                'worker-name': lambda _: str(
                    user_table[notification.worker_id].full_name
                ),
                'birth-date': lambda _: str(
                    user_table[notification.worker_id].birth_date
                ),
                'point-name': lambda _: str(
                    points_table[notification.owner_id][
                        simple_vacancies_table[notification.owner_id][
                            notification.vacancy_id
                        ].point_id
                    ].name
                ),
            },
        ),
        keyboard=keyboard(
            (
                RowInfo(factory.saved(WorkHiveButton.Ok))
                if len(notifications) == 0
                else RowInfo(
                    factory.saved(WorkHiveButton.Accept, args=('accept', index)),
                    factory.saved(WorkHiveButton.Decline, args=('decline', index)),
                )
            ),
            RowInfo(
                (
                    factory.saved(WorkHiveButton.Back, args=('back', index))
                    if int(index) > 0
                    else None
                ),
                (
                    factory.saved(WorkHiveButton.Next, args=('next', index))
                    if int(index) < len(notifications) - 1
                    else None
                ),
            ),
        ),
    )

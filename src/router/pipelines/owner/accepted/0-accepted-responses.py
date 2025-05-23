from telebot.types import LinkPreviewOptions

from model.tables import (
    _Point,
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


def get_notification(owner: Owner, index: str) -> _Response | None:
    notifications: list[_Response] = [
        response_map[response.__sql_id__]
        for response in responses_table[owner.workhive_id].values()
        if response_map[response.__sql_id__].status == 'accepted'
        and not response_map[response.__sql_id__].is_expired
    ]
    if index == str():
        index = '0'
    return notifications[int(index)] if len(notifications) > 0 else None


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


def change_status(response: _Response, new_status: str) -> None:
    response.status = new_status
    response_map.update({response.response_id: response})


@router.add(
    name=FSAState.OwnerAcceptedResponses,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.MainMenu: FSAState.OwnerMainMenu,
        FSASymbol.Delete: FSAState.OwnerMainMenu,
        FSASymbol.Next: FSAState.OwnerAcceptedResponses,
        FSASymbol.Back: FSAState.OwnerAcceptedResponses,
        FSASymbol.Ok: FSAState.OwnerMainMenu,
    },
)
def owner_settings(
    owner: Owner, factory: ButtonFactoryClosure, action: str, index: str
) -> TGMessage:
    notification: _Response | None = get_notification(owner, index)
    match action:
        case 'undefined':
            assert notification is not None
            change_status(notification, 'undefined')
        case 'next':
            index = str(int(index) + 1)
        case 'back':
            index = str(int(index) - 1)
    notification = get_notification(owner, index)
    point: _Point | None = (
        points_table[notification.owner_id][
            simple_vacancies_table[notification.owner_id][
                notification.vacancy_id
            ].point_id
        ]
        if notification is not None
        else None
    )
    if notification is not None:
        notification.is_read_by_owner = True
        response_map.update({notification.response_id: notification})
    message: TGMessage = TGMessage(
        text=render_file(
            language=owner.language,
            state=(
                owner.state
                if notification is not None
                and point is not None
                and response_map[notification.response_id].status == 'accepted'
                else FSAState.OwnerNoAcceptedResponses
            ),
            tag_handlers=(
                {
                    'point-name': lambda _: f'<b>{point.name}</b>',
                    'address': lambda _: (
                        f'<a href=\"{point.yandex_link}\">{point.address}</a>'
                    ),
                    'payload': lambda _: str(point.payload),
                    'minimal-charge': lambda _: str(point.minimal_charge),
                    'charge-per-one': lambda _: (
                        f'{point.charge_per_one // 100}.{(
                            '0' if point.charge_per_one % 100 < 10 else str()
                        )}{point.charge_per_one % 100}'
                    ),
                    'id': lambda _: f'<i>{str(notification.vacancy_id)[:6]}</i>',
                    'worker-name': lambda _: str(
                        user_table[notification.worker_id].full_name
                    ),
                    'birth-date': lambda _: user_table[
                        notification.worker_id
                    ].birth_date.strftime('%d-%m-%Y'),
                    'mention': lambda placeholder: (
                        f'<a href=\"tg://user?id={
                            notification.worker_telegram_id
                        }\">{placeholder}</a>'
                    ),
                }
                if notification is not None
                and point is not None
                and response_map[notification.response_id].status == 'accepted'
                else None
            ),
        ),
        keyboard=keyboard(
            *(
                (RowInfo(factory.saved(WorkHiveButton.Ok)),)
                if notification is None
                else (RowInfo(factory.saved(WorkHiveButton.MainMenu)),)
            ),
            (
                RowInfo(
                    (
                        factory.saved(WorkHiveButton.LeftArrow, args=('back', index))
                        if int(index) > 0
                        else None
                    ),
                    (
                        factory.saved(WorkHiveButton.RightArrow, args=('next', index))
                        if int(index)
                        < len(
                            [
                                response
                                for response in responses_table[
                                    owner.workhive_id
                                ].values()
                                if response_map[response.__sql_id__].status
                                == 'accepted'
                            ]
                        )
                        - 1
                        else None
                    ),
                )
                if notification is not None
                else None
            ),
        ),
        link_preview=LinkPreviewOptions(is_disabled=True),
    )
    return message

from uuid import UUID

from model.tables import (
    _Point,
    _Response,
    points_table,
    response_map,
    responses_table,
    simple_vacancies_table,
)
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


def get_responses(owner: Owner, point: _Point) -> list[_Response]:
    return [
        response_map[response.__sql_id__]
        for response in responses_table[owner.workhive_id].values()
        if simple_vacancies_table[response_map[response.__sql_id__].vacancy_id][
            owner.workhive_id
        ].point_id
        == point.__sql_id__
    ]


def delete_responses(owner: Owner, ids: list[UUID]) -> None:
    responses: list[_Response] = [
        response_map[id.__sql_id__]
        for id in responses_table[owner.workhive_id].values()
        if id.__sql_id__ in ids
    ]
    for response in responses:
        responses_table.remove_one(response.owner_id, response.response_id)
        responses_table.remove_one(response.vacancy_id, response.response_id)
        # responses_table.remove_one(response.point_id, response.response_id)
        responses_table.remove_one(response.worker_id, response.response_id)
        response_map.remove(response.response_id)


@router.add(
    name=FSAState.OwnerPointDeleted,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Ok: FSAState.OwnerPoints,
    },
)
def owner_point_deleted(
    owner: Owner, factory: ButtonFactoryClosure, index: str, delete: bool
) -> TGMessage:
    point: _Point | None = (
        list(owner.points.values())[int(index)] if index != str() else None
    )
    if point is not None and delete:
        points_table.remove_one(owner.workhive_id, point.__sql_id__)
        for vacancy in owner.simple_vacancies.values():
            if vacancy.point_id == point.__sql_id__:
                simple_vacancies_table.remove_one(owner.workhive_id, vacancy.__sql_id__)
                response_ids: list[UUID] = [
                    response_id
                    for response_id in responses_table[owner.workhive_id]
                    if response_map[response_id].vacancy_id == vacancy.__sql_id__
                ]
                delete_responses(owner, response_ids)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state if not delete else FSAState.OwnerPointDeleted,
            tag_handlers=(
                {
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
                    'point-name': lambda _: f'<b>{(point.name)}</b>',
                }
                if point is not None
                else None
            ),
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Ok)),
        ),
    )

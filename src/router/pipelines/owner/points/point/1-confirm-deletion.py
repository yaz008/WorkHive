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


def delete_response(response: _Response) -> None:
    responses_table.remove_one(response.owner_id, response.response_id)
    responses_table.remove_one(response.vacancy_id, response.response_id)
    # responses_table.remove_one(response.point_id, response.response_id)
    responses_table.remove_one(response.worker_id, response.response_id)
    response_map.remove(response.response_id)


@router.add(
    name=FSAState.OwnerPointDeletionConfirm,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Yes: FSAState.OwnerPointDeleted,
        FSASymbol.No: FSAState.OwnerPoints,
    },
)
def owner_point_deletion(
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
        for response in get_responses(owner, point):
            delete_response(response)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state if not delete else FSAState.OwnerPointDeleted,
            tag_handlers=(
                {
                    'link': lambda placeholder: (
                        point.yandex_link
                        if point.yandex_link is not None
                        else placeholder
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
            RowInfo(factory.saved(WorkHiveButton.Yes, args=(index, True))),
            RowInfo(factory.saved(WorkHiveButton.No, args=(index, False))),
        ),
    )

from model.tables import (
    _Point,
    _Response,
    points_table,
    simple_vacancies_table,
    responses_table,
    response_map,
)
from model.types import Worker
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.utils import in_metadata, add_metadata


def delete_response(worker: Worker, index: str) -> None:
    if index != str():
        response: _Response = [
            response_map[id.__sql_id__]
            for id in responses_table[worker.workhive_id].values()
        ][int(index)]
        responses_table.remove_one(response.owner_id, response.response_id)
        responses_table.remove_one(response.vacancy_id, response.response_id)
        # responses_table.remove_one(response.point_id, response.response_id)
        responses_table.remove_one(response.worker_id, response.response_id)
        response_map.remove(response.response_id)


def get_current_response(responses: list[_Response], index: str) -> _Response | None:
    return responses[int(index)] if len(responses) > 0 else None


@router.add(
    name=FSAState.WorkerAcceptedResponds,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.MainMenu: FSAState.WorkerMainMenu,
        FSASymbol.Next: FSAState.WorkerAcceptedResponds,
        FSASymbol.Back: FSAState.WorkerAcceptedResponds,
        FSASymbol.Delete: FSAState.WorkerAcceptedResponds,
    },
)
def owner_point_payload(
    worker: Worker, factory: ButtonFactoryClosure, action: str, index: str
) -> TGMessage:
    if not in_metadata(worker, 'has-opened-accepted'):
        add_metadata(worker, 'has-opened-accepted')
    if action == 'back':
        index = str(int(index) - 1)
    if action == 'next':
        index = str(int(index) + 1)
    if action == 'delete':
        delete_response(worker, index)
    responses: list[_Response] = [
        response_map[id.__sql_id__]
        for id in responses_table[worker.workhive_id].values()
        if response_map[id.__sql_id__].status == 'accepted'
    ]
    response: _Response | None = get_current_response(responses, index)
    if response is not None:
        response.is_read_by_worker = True
        response_map.update({response.response_id: response})
    point: _Point | None = (
        points_table[response.owner_id][
            simple_vacancies_table[response.owner_id][response.vacancy_id].point_id
        ]
        if response is not None
        else None
    )
    return TGMessage(
        text=render_file(
            language=worker.language,
            state=(
                worker.state
                if response is not None
                else FSAState.WorkerNoAcceptedResponds
            ),
            tag_handlers=(
                {
                    'franchise': lambda _: point.franchise,
                    'address': lambda _: (
                        f'<a href="{point.yandex_link}">{point.address}</a>'
                    ),
                    'payload': lambda _: str(point.payload),
                    'minimal-charge': lambda _: str(point.minimal_charge),
                    'charge-per-one': lambda _: (
                        f'{point.charge_per_one // 100}.{point.charge_per_one % 100}'
                    ),
                }
                if point is not None
                else None
            ),
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.MainMenu)),
            (
                RowInfo(factory.saved(WorkHiveButton.Delete, args=('delete', index)))
                if response is not None
                else None
            ),
            RowInfo(
                (
                    factory.saved(WorkHiveButton.LeftArrow, args=('back', index))
                    if int(index) > 0
                    else None
                ),
                (
                    factory.saved(WorkHiveButton.RightArrow, args=('next', index))
                    if len(responses) > int(index) + 1
                    else None
                ),
            ),
        ),
    )

from model.tables import (
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


def delete_response(worker: Worker, index: str) -> None:
    if index != str():
        response: _Response = [
            response_map[id.__sql_id__]
            for id in responses_table[worker.workhive_id].values()
        ][int(index)]
        responses_table.remove_one(response.owner_id, response.response_id)
        responses_table.remove_one(response.vacancy_id, response.response_id)
        responses_table.remove_one(response.worker_id, response.response_id)
        response_map.remove(response.response_id)


@router.add(
    name=FSAState.WorkerResponds,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.Back: FSAState.WorkerMainMenu,
        FSASymbol.Delete: FSAState.WorkerResponds,
    },
)
def owner_point_payload(
    worker: Worker, factory: ButtonFactoryClosure, index: str
) -> TGMessage:
    delete_response(worker, index)
    responses: list[_Response] = [
        response_map[id.__sql_id__]
        for id in responses_table[worker.workhive_id].values()
    ]
    return TGMessage(
        text=render_file(
            language=worker.language,
            state=worker.state,
        ),
        keyboard=keyboard(
            *(
                RowInfo(
                    factory.create(
                        symbol=FSASymbol.Delete,
                        name=points_table[response.owner_id][
                            simple_vacancies_table[response.owner_id][
                                response.vacancy_id
                            ].point_id
                        ].address[:25],
                        args=(responses.index(response),),
                        load=False,
                    )
                )
                for response in responses
            ),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

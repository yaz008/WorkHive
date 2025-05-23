from uuid import UUID

from model.tables import (
    _VacancySimple,
    _Response,
    simple_vacancies_table,
    responses_table,
    response_map,
)
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


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
    name=FSAState.OwnerVacancyDelete,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerVacancies,
        FSASymbol.Delete: FSAState.OwnerVacancyDelete,
    },
)
def owner_point_payload(
    owner: Owner, factory: ButtonFactoryClosure, index: str
) -> TGMessage:
    if index != str():
        vacancy: _VacancySimple | None = simple_vacancies_table.pop_one(
            owner.workhive_id,
            list(owner.simple_vacancies.values())[int(index)].__sql_id__,
        )
        if vacancy is not None:
            response_ids: list[UUID] = [
                response_id
                for response_id in responses_table[owner.workhive_id]
                if response_map[response_id].vacancy_id == vacancy.__sql_id__
            ]
            delete_responses(owner, response_ids)

    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
        ),
        keyboard=keyboard(
            *(
                RowInfo(
                    factory.create(
                        symbol=FSASymbol.Delete,
                        name=' '.join(
                            (
                                f'{owner.points[vacancy.point_id].name}',
                                f'({str(vacancy.__sql_id__)[:6]})',
                            )
                        ),
                        args=(list(owner.simple_vacancies.values()).index(vacancy),),
                        load=False,
                    )
                )
                for vacancy in owner.simple_vacancies.values()
            ),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

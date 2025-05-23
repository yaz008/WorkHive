from itertools import chain
from uuid import uuid4, UUID

from telebot.types import LinkPreviewOptions

from driver import driver
from model.tables import (
    _VacancySimple,
    _SearchResult,
    _Point,
    _Response,
    search_results_table,
    points_table,
    responses_table,
    response_map,
    simple_vacancies_table,
    tgid_table,
)
from model.types import Worker
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.orm import Stackable
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router import router
from router.pipelines.utils import in_metadata, add_metadata


def search(workhive_id: UUID) -> _SearchResult:
    if (
        workhive_id not in search_results_table.keys()
        or search_results_table[workhive_id].is_expired
    ):
        search_results_table.update(
            {
                workhive_id: _SearchResult(
                    vacancies=tuple(
                        vacancy
                        for vacancy in chain(
                            *map(lambda d: d.values(), simple_vacancies_table.values)
                        )
                        if not vacancy.is_expired
                    )
                )
            }
        )
    return search_results_table[workhive_id]


def respond(vacancy: _VacancySimple, worker: Worker) -> None:
    response_id: UUID = uuid4()
    response: _Response = _Response(
        response_id=response_id,
        vacancy_id=vacancy.__sql_id__,
        owner_id=vacancy.owner_id,
        worker_id=worker.workhive_id,
        worker_telegram_id=worker.telegram_id,
    )
    response_map.update({response_id: response})
    responses_table.update(
        {
            worker.workhive_id: Stackable(__sql_id__=response_id),
            vacancy.owner_id: Stackable(__sql_id__=response_id),
            vacancy.__sql_id__: Stackable(__sql_id__=response_id),
        }
    )
    driver.notify(
        target_id=tgid_table[response.owner_id].value,
        message=TGMessage(
            text=f'Отклик на <code>{
                points_table[vacancy.owner_id][vacancy.point_id].name
            }</code> <i>({
                str(vacancy.__sql_id__)[:6]
            })</i>! Нажмите /start, чтобы посмотреть',
        ),
    )


def update_index(worker: Worker, result: _SearchResult, arg: str) -> None:
    if result.current_index is not None:
        match arg:
            case 'back':
                result.current_index -= 1
            case 'next':
                result.current_index += 1
    else:
        result.current_index = 0
    search_results_table.update({worker.workhive_id: result})


@router.add(
    name=FSAState.WorkerSearchResults,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.Respond: FSAState.WorkerSearchResults,
        FSASymbol.Next: FSAState.WorkerSearchResults,
        FSASymbol.Back: FSAState.WorkerSearchResults,
        FSASymbol.Ok: FSAState.WorkerMainMenu,
        FSASymbol.MainMenu: FSAState.WorkerMainMenu,
    },
)
def owner_settings(
    worker: Worker, factory: ButtonFactoryClosure, arg: str
) -> TGMessage:
    if not in_metadata(worker, 'has-searched'):
        add_metadata(worker, 'has-searched')
    result: _SearchResult = search(worker.workhive_id)
    update_index(worker, result, arg)
    assert result.current_index is not None
    vacancy: _VacancySimple | None = (
        result.vacancies[result.current_index] if len(result.vacancies) > 0 else None
    )
    if vacancy is not None:
        if arg == 'respond':
            respond(vacancy, worker)
    point: _Point | None = (
        points_table[vacancy.owner_id][vacancy.point_id]
        if vacancy is not None
        else None
    )
    return TGMessage(
        text=render_file(
            language=worker.language,
            state=(
                worker.state
                if len(result.vacancies) > 0
                else FSAState.WorkerSearchNoResults
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
                        f'{point.charge_per_one // 100}.{(
                            '0' if point.charge_per_one % 100 < 10 else str()
                        )}{point.charge_per_one % 100}'
                    ),
                    'expected-payment': lambda _: point.expected_payment,
                    'vacancy-id': lambda _: f'<i>{str(vacancy.__sql_id__)[:6]}</i>',
                }
                if vacancy is not None and point is not None
                else None
            ),
        ),
        keyboard=keyboard(
            RowInfo(
                None
                if len(result.vacancies) == 0
                else (
                    factory.saved(WorkHiveButton.Respond, args=('respond',))
                    if (
                        vacancy is not None
                        and vacancy.__sql_id__
                        not in [
                            response_map[id.__sql_id__].vacancy_id
                            for id in responses_table[worker.workhive_id].values()
                        ]
                    )
                    else None
                )
            ),
            RowInfo(
                (
                    factory.saved(WorkHiveButton.LeftArrow, args=('back',))
                    if result.current_index > 0
                    else None
                ),
                (
                    factory.saved(WorkHiveButton.RightArrow, args=('next',))
                    if result.current_index < len(result.vacancies) - 1
                    else None
                ),
            ),
            RowInfo(factory.saved(WorkHiveButton.MainMenu)),
        ),
        link_preview=LinkPreviewOptions(prefer_small_media=True, show_above_text=True),
    )

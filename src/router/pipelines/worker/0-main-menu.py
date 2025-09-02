from typing import Final

from model.tables import (
    _Response,
    temp_users,
    responses_table,
    response_map,
)
from model.types import User, TempUser, create_user
from project.configs import FSASymbol, FSAState, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.utils import in_metadata


PAMPADU_LINK: Final[str] = 'https://forchampion.ru/cea2ed86-b64a-4577-903f-b56d00657916'
OZON_LINK: Final[str] = (
    f'https://recruitment.ozon.ru/predstavitel-bank/?{(
        '&'.join(
            [
                'customer=fintech',
                'vacancy=mobileAmbassador',
                'channel=leadgens',
                'source=liger',
                'utm_source=liger',
                'leadType=reply',
                '__rr=1',
            ]
        )
    )}'
)


@router.add(
    name=FSAState.WorkerMainMenu,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.Settings: FSAState.WorkerSettings,
        FSASymbol.Search: FSAState.WorkerSearchResults,
        FSASymbol.Responds: FSAState.WorkerResponds,
        FSASymbol.AcceptedResponses: FSAState.WorkerAcceptedResponds,
    },
)
def worker_main_menu(user: User | TempUser, factory: ButtonFactoryClosure) -> TGMessage:
    if isinstance(user, TempUser):
        user = create_user(user)
        temp_users.remove(user.telegram_id)
    responses: list[_Response] = [
        response_map[id.__sql_id__]
        for id in responses_table[user.workhive_id].values()
        if response_map[id.__sql_id__].status == 'accepted'
    ]
    return TGMessage(
        text=render_file(
            language=user.language,
            state=(
                user.state
                if all(
                    in_metadata(user, value)
                    for value in (
                        'has-searched',
                        'has-opened-responses',
                        'has-opened-accepted',
                    )
                )
                else 'worker-main-menu-fst'
            ),
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Search)),
            RowInfo(factory.saved(name=WorkHiveButton.MoreVacancies, url=PAMPADU_LINK)),
            RowInfo(
                factory.saved(name=WorkHiveButton.PROMO_OzonVacancies, url=OZON_LINK)
            ),
            RowInfo(
                factory.saved(WorkHiveButton.MyResponds, args=(str(), '0')),
                factory.saved(
                    (
                        WorkHiveButton.AcceptedResponsesNew
                        if any(not response.is_read_by_worker for response in responses)
                        else WorkHiveButton.AcceptedResponses
                    ),
                    args=(str(), '0'),
                ),
            ),
            RowInfo(factory.saved(WorkHiveButton.Settings)),
        ),
    )

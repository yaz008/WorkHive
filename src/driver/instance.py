from typing import Literal, cast, assert_never

from telebot.types import InlineKeyboardMarkup
from telebot.util import quick_markup

from model.tables import user_table, workhive_id, temp_users, role_table, state_table
from project.configs import TGDriverConfig, ChennelConfig, FSAState
from project.core.env import Env
from project.libs.tgdraw import TGDriver
from project.libs.tght import render_file


Role = Literal['worker', 'owner', 'temp']


def get_keyboard(telegram_id: int) -> InlineKeyboardMarkup | None:
    role: Role = cast(
        Role,
        (
            role_table[workhive_id[telegram_id].value].role
            if telegram_id not in temp_users
            else 'temp'
        ),
    )
    state: str = state_table[workhive_id[telegram_id].value].state
    if state in (FSAState.WorkerNoADConsent, FSAState.OwnerNoADConsent):
        return None
    match role:
        case 'worker':
            return quick_markup(
                values={
                    'Подпишись на наш канал!': {'url': ChennelConfig.WorkersChannelLink}
                },
                row_width=1,
            )
        case 'owner':
            return quick_markup(
                values={
                    'Подпишись на наш канал!': {'url': ChennelConfig.OwnersChannelLink},
                },
                row_width=1,
            )
        case 'temp':
            return InlineKeyboardMarkup()
        case _:
            assert_never(role)


driver: TGDriver = TGDriver(
    token=Env.TELEGRAM_BOT_TOKEN,
    parse_mode=TGDriverConfig.DefaultParseMode,
    skip_pending=TGDriverConfig.SkipPending,
    threads=TGDriverConfig.Threads,
    is_threaded=TGDriverConfig.IsThreaded,
    on_session_expiration=lambda session: cast(
        None,
        driver.send_message(
            chat_id=session.telegram_id,
            text=render_file(
                language=(
                    user_table[workhive_id[session.telegram_id].value].language
                    if session.telegram_id not in temp_users
                    else temp_users[session.telegram_id].value['language']
                ),
                state=f'driver-on-{(
                    role_table[workhive_id[session.telegram_id].value].role
                    if session.telegram_id not in temp_users
                    else 'temp'
                )}-session-expiration',
            ),
            reply_markup=get_keyboard(session.telegram_id),
        ),
    ),
)

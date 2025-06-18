from typing import cast

from telebot.util import quick_markup

from model.tables import user_table, workhive_id, temp_users, role_table
from project.configs import TGDriverConfig, ChennelConfig
from project.core.env import Env
from project.libs.tgdraw import TGDriver
from project.libs.tght import render_file


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
                state='driver-on-session-expiration',
                tag_handlers={
                    'channel': lambda _: (
                        f'Подпишитесь на наш канал: {(
                            ChennelConfig.WorkersChannelLink
                            if role_table[workhive_id[session.telegram_id].value].role
                            == 'worker'
                            else ChennelConfig.OwnersChannelLink
                        )}'
                        if session.telegram_id not in temp_users
                        else str()
                    )
                },
            ),
            reply_markup=quick_markup(
                values={
                    'Подпишись на наш канал!': {
                        'url': (
                            ChennelConfig.WorkersChannelLink
                            if role_table[workhive_id[session.telegram_id].value].role
                            == 'worker'
                            else ChennelConfig.OwnersChannelLink
                        )
                    }
                },
                row_width=1,
            ),
        ),
    ),
)

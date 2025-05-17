from model.tables import user_table, workhive_id, temp_users
from project.configs import TGDriverConfig
from project.core.env import Env
from project.libs.tgdraw import TGDriver
from project.libs.tght import render_file


driver: TGDriver = TGDriver(
    token=Env.TELEGRAM_BOT_TOKEN,
    parse_mode=TGDriverConfig.DefaultParseMode,
    skip_pending=TGDriverConfig.SkipPending,
    threads=TGDriverConfig.Threads,
    is_threaded=TGDriverConfig.IsThreaded,
    on_session_expiration=lambda session: driver.send_message(
        chat_id=session.telegram_id,
        text=render_file(
            language=(
                user_table[workhive_id[session.telegram_id].value].language
                if session.telegram_id not in temp_users
                else temp_users[session.telegram_id].value['language']
            ),
            state='driver-on-session-expiration',
        ),
    ),
)

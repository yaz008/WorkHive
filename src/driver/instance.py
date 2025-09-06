from random import random
from typing import Literal, Final, cast, assert_never

from telebot.types import InlineKeyboardMarkup, LinkPreviewOptions
from telebot.util import quick_markup

from model.tables import (
    user_table,
    workhive_id,
    temp_users,
    role_table,
    state_table,
    response_map,
    responses_table,
    _Response,
)
from model.types import User, Owner, Worker
from project.configs import (
    TGDriverConfig,
    ChennelConfig,
    FSAState,
    WorkHiveButton,
    SessionConfig,
)
from project.core.env import Env
from project.libs.tgdraw import TGDriver, load_button
from project.libs.tgdraw.driver.session import Session
from project.libs.tght import render_file


Role = Literal['worker', 'owner', 'temp']
MessageKind = Literal['session-expiration', 'new-notification']


TRANSITION_LINK: Final[str] = (
    f'https://docs.google.com/presentation/d/{(
        '14fs4QUIOpWyIOKRWORgS3m2TFnvta_0eSdKMQqIGkoI'
    )}/edit?usp=sharing'
)


def get_user_role(telegram_id: int) -> Role:
    return cast(
        Role,
        (
            role_table[workhive_id[telegram_id].value].role
            if telegram_id not in temp_users
            else 'temp'
        ),
    )


def get_keyboard(telegram_id: int) -> InlineKeyboardMarkup | None:
    role: Role = get_user_role(telegram_id)
    state: str = state_table[workhive_id[telegram_id].value].state
    subsribe_button: str = load_button(
        WorkHiveButton.SubscribeToOurChannel,
        language=user_table[workhive_id[telegram_id].value].language,
    )
    easy_transition: str = load_button(
        WorkHiveButton.PROMO_EasyTransition,
        language=user_table[workhive_id[telegram_id].value].language,
    )
    if state in (FSAState.WorkerNoADConsent, FSAState.OwnerNoADConsent):
        return None
    match role:
        case 'worker':
            return quick_markup(
                values={subsribe_button: {'url': ChennelConfig.WorkersChannelLink}},
                row_width=1,
            )
        case 'owner':
            return quick_markup(
                values={
                    subsribe_button: {'url': ChennelConfig.OwnersChannelLink},
                    easy_transition: {'url': TRANSITION_LINK},
                },
                row_width=1,
            )
        case 'temp':
            return InlineKeyboardMarkup()
        case _:
            assert_never(role)


def get_notifications(user: User, status: str) -> list[_Response]:
    return [
        response_map[response.__sql_id__]
        for response in responses_table[user.workhive_id].values()
        if response_map[response.__sql_id__].status == status
    ]


def get_message_kind(session: Session, role: Role) -> MessageKind:
    return (
        'session-expiration'
        if (
            role == 'temp'
            or (
                role == 'owner'
                and not any(
                    not notification.is_read_by_owner
                    for notification in get_notifications(
                        Owner(session.telegram_id), status='undefined'
                    )
                    if not notification.is_expired
                )
            )
            or (
                role == 'worker'
                and not any(
                    not notification.is_read_by_worker
                    for notification in get_notifications(
                        Worker(session.telegram_id), status='accepted'
                    )
                    if not notification.is_expired
                )
            )
        )
        else 'new-notification'
    )


def on_session_expiration(session: Session) -> None:
    role: Role = get_user_role(session.telegram_id)
    message_kind: MessageKind = get_message_kind(session, role)
    if (
        message_kind == 'new-notification'
        or SessionConfig.OnExpirationMessageProbability > random()
    ):
        driver.send_message(
            chat_id=session.telegram_id,
            text=render_file(
                language=(
                    user_table[workhive_id[session.telegram_id].value].language
                    if session.telegram_id not in temp_users
                    else temp_users[session.telegram_id].value['language']
                ),
                state=f'driver-on-{role}-{message_kind}',
            ),
            reply_markup=(
                get_keyboard(session.telegram_id)
                if message_kind == 'session-expiration'
                else None
            ),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )


driver: TGDriver = TGDriver(
    token=Env.TELEGRAM_BOT_TOKEN,
    parse_mode=TGDriverConfig.DefaultParseMode,
    skip_pending=TGDriverConfig.SkipPending,
    threads=TGDriverConfig.Threads,
    is_threaded=TGDriverConfig.IsThreaded,
    on_session_expiration=on_session_expiration,
)

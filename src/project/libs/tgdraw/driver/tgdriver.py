from dataclasses import dataclass, field
from datetime import datetime
from random import random
from typing import Any, Callable, cast

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from telebot import TeleBot, logging
from telebot.apihelper import ApiTelegramException
from telebot.types import Message

from model.tables import _Metadata, temp_users, user_table, workhive_id, metadata_table
from project.configs import (
    TableConfig,
    CacheSizeConfig,
    TGDriverConfig,
    VerboseConfig,
    SessionConfig,
    TGParseMode,
)
from project.libs.err import ignore_error
from project.libs.orm import CachedSingleTable
from project.libs.tgdraw.driver.session import Session
from project.libs.tgdraw.types import TGMessage, MessageKind
from project.libs.verbose import verbose


@dataclass(slots=True)
class TGDriver(TeleBot):
    on_session_expiration: Callable[[Session], None]
    __session_table: CachedSingleTable[int, Session] = field(init=False)
    __scheduler: BackgroundScheduler = field(init=False)

    def __init__(
        self,
        token: str,
        parse_mode: TGParseMode,
        skip_pending: bool,
        is_threaded: bool,
        threads: int,
        on_session_expiration: Callable[[Session], None] = lambda _: None,
    ) -> None:
        self.on_session_expiration = on_session_expiration
        self.__session_table = CachedSingleTable(
            database=TableConfig.Sessions.database,
            table=TableConfig.Sessions.table,
            key_cls=int,
            value_cls=Session,
            cache_size=CacheSizeConfig.SessionTable,
        )
        self.__scheduler = BackgroundScheduler()
        self.__scheduler.start()
        super(TGDriver, self).__init__(
            token=token,
            parse_mode=parse_mode,
            skip_pending=skip_pending,
            num_threads=threads,
            threaded=is_threaded,
        )

    @ignore_error(ApiTelegramException, return_error=True)
    def __update_session(self, telegram_id: int, message: TGMessage) -> Session:
        if telegram_id not in self.__session_table.keys:
            return self.create(telegram_id, message)
        session: Session = self.__session_table[telegram_id]
        common_params: dict[str, Any] = {
            'chat_id': session.telegram_id,
            'message_id': session.message_id,
            'reply_markup': message.markup,
        }
        if message.kind == 'Text':
            if session.kind == 'Text':
                self.edit_message_text(
                    **{
                        'text': message.text,
                        'link_preview_options': message.link_preview,
                    }
                    | common_params
                )
            else:
                self.revoke(session)
                return self.create(telegram_id, message)
        else:
            self.edit_message_media(**{'media': message.media} | common_params)
        session.kind = message.kind
        session.last_accessed = datetime.now()
        return session

    def update(self, telegram_id: int, message: TGMessage) -> None:
        maybe_session: Session | ApiTelegramException = self.__update_session(
            telegram_id, message
        )
        if not (
            isinstance(maybe_session, ApiTelegramException)
            and 'message to edit not found' not in maybe_session.description
        ):
            session: Session = (
                maybe_session
                if isinstance(maybe_session, Session)
                else (self.create(telegram_id, message))
            )
            self.__session_table.update({telegram_id: session})
            self.__scheduler.add_job(
                self.revoke,
                trigger=DateTrigger(
                    min(
                        session.last_accessed + SessionConfig.ActiveLifeTime,
                        session.expiration_time,
                    )
                ),
                args=[session, True],
                id=str(telegram_id),
                replace_existing=True,
            )

    def create(self, telegram_id: int, message: TGMessage) -> Session:
        session_message: Message = cast(
            dict[MessageKind, Callable[..., Message]],
            {
                'Animation': self.send_animation,
                'Document': self.send_document,
                'Audio': self.send_audio,
                'Photo': self.send_photo,
                'Video': self.send_video,
                'Text': self.send_message,
            },
        )[message.kind](
            **(
                (
                    {
                        message.kind.lower(): message.tgmedia.file_id,
                        'caption': message.text,
                    }
                )
                if message.tgmedia is not None
                else cast(
                    dict[str, Any | None],
                    {
                        'text': message.text,
                        'link_preview_options': message.link_preview,
                    },
                )
            )
            | {
                'chat_id': telegram_id,
                'reply_markup': message.markup,
            }
        )
        return Session(
            telegram_id=telegram_id, message_id=session_message.id, kind=message.kind
        )

    def notify(self, target_id: int, message: TGMessage) -> None:
        if target_id not in self.__session_table.keys:
            self.update(telegram_id=target_id, message=message)

    @ignore_error(ApiTelegramException)
    def revoke(self, session: Session, is_expired: bool = False) -> None:
        self.__session_table.remove(session.telegram_id)
        self.delete_message(chat_id=session.telegram_id, message_id=session.message_id)
        if is_expired and (
            session.telegram_id in temp_users
            or SessionConfig.OnExpirationMessageProbability > random()
            or (
                workhive_id[session.telegram_id].value in user_table
                and 'has-start-message'
                not in map(
                    lambda m: m.value,
                    metadata_table[workhive_id[session.telegram_id].value].values(),
                )
            )
        ):
            if session.telegram_id not in temp_users:
                metadata_table.update(
                    {
                        workhive_id[session.telegram_id].value: _Metadata(
                            'has-start-message'
                        )
                    }
                )
            self.on_session_expiration(session)

    @verbose(before=TGDriverConfig.OnBotStart, level=VerboseConfig.Level)
    def infinity_polling(
        self,
        timeout=20,
        skip_pending=False,
        long_polling_timeout=20,
        logger_level=logging.ERROR,
        allowed_updates=None,
        restart_on_change=False,
        path_to_watch=None,
        *args,
        **kwargs,
    ):
        return super(TGDriver, self).infinity_polling(
            timeout,
            skip_pending,
            long_polling_timeout,
            logger_level,
            allowed_updates,
            restart_on_change,
            path_to_watch,
            *args,
            **kwargs,
        )

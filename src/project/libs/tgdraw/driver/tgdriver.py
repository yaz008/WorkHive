from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import Message

from project.configs import TableConfig, CacheSizeConfig, SessionConfig, TGParseMode
from project.libs.err import ignore_error
from project.libs.orm import CachedSingleTable
from project.libs.tgdraw.driver.session import Session
from project.libs.tgdraw.types import TGMessage


@dataclass(slots=True)
class TGDriver(TeleBot):
    __session_table: CachedSingleTable[int, Session] = field(init=False)
    __scheduler: BackgroundScheduler = field(init=False)

    def __init__(
        self,
        token: str,
        parse_mode: TGParseMode,
        skip_pending: bool,
        threads: int,
    ) -> None:
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
            threaded=(threads > 1),
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
                self.edit_message_text(**{'text': message.text} | common_params)
            else:
                self.revoke(session)
                return self.create(telegram_id, message)
        else:
            self.edit_message_media(**{'media': message.media} | common_params)
        session.kind = message.kind
        session.last_accessed = datetime.now()
        return session

    def has_active_session(self, telegram_id: int) -> bool:
        return telegram_id in self.__session_table.keys

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
                args=[session],
                id=str(telegram_id),
                replace_existing=True,
            )

    def create(self, telegram_id: int, message: TGMessage) -> Session:
        session_message: Message = {
            'Animation': self.send_animation,
            'Document': self.send_document,
            'Audio': self.send_audio,
            'Photo': self.send_photo,
            'Video': self.send_video,
        }.get(message.kind, self.send_message)(
            **(
                {message.kind.lower(): message.media_bin, 'caption': message.text}
                if message.media_bin
                else {'text': message.text}
            )
            | {
                'chat_id': telegram_id,
                'reply_markup': message.markup,
            }
        )
        return Session(
            telegram_id=telegram_id, message_id=session_message.id, kind=message.kind
        )

    @ignore_error(ApiTelegramException)
    def revoke(self, session: Session) -> None:
        self.__session_table.remove(session.telegram_id)
        self.delete_message(chat_id=session.telegram_id, message_id=session.message_id)

from typing import Callable

from telebot.types import Message, CallbackQuery

from model.tables import workhive_id, temp_users
from model.types import User, TempUser
from project.libs.orm import TempValue


def get_user(telegram_id: int) -> User | TempUser:
    if telegram_id not in workhive_id.keys:
        if telegram_id not in temp_users.keys:
            temp_users.update({telegram_id: TempValue()})
            return TempUser(telegram_id, set_default=True)
        return TempUser(telegram_id)
    return User(telegram_id=telegram_id)


def register(
    on_start: Callable[[User | TempUser], None],
) -> Callable[[Message], None]:
    def wrapper(message: Message) -> None:
        return on_start(get_user(message.chat.id))

    return wrapper


def with_user(
    handler: Callable[[User | TempUser, Message | CallbackQuery], None],
) -> Callable[[Message], None]:
    def wrapper(__input: Message | CallbackQuery, /) -> None:
        telegram_id: int = (
            __input.chat.id if isinstance(__input, Message) else __input.from_user.id
        )
        return handler(get_user(telegram_id), __input)

    return wrapper

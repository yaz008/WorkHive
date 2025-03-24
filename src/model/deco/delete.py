from typing import Callable

from telebot.types import Message

from driver import driver


def delete_message(handler: Callable[[Message], None]) -> Callable[[Message], None]:
    def wrapper(message: Message) -> None:
        driver.delete_message(chat_id=message.chat.id, message_id=message.id)
        return handler(message)

    return wrapper

from typing import Callable

from telebot.types import Message

from model.blacklist.load import load_blacklist
from project.configs import BlacklistConfig


def blacklist(func: Callable[[Message], None]) -> Callable[[Message], None]:
    banned: set[int] = load_blacklist(
        path=f'{BlacklistConfig.BasePath}/{BlacklistConfig.Filename}',
    )

    def wrapper(message: Message) -> None:
        if message.from_user.id not in banned:
            func(message)

    return wrapper if len(banned) > 0 else func

from typing import Callable

from telebot.types import Message

from model.blacklist.load import load_blacklist


def blacklist(
    path: str, on_block: Callable[[Message], None] = lambda _: None
) -> Callable[[Callable[[Message], None]], Callable[[Message], None]]:
    def decorator(func: Callable[[Message], None]) -> Callable[[Message], None]:
        banned: set[int] = load_blacklist(path=path)

        def wrapper(message: Message) -> None:
            if message.from_user.id not in banned:
                func(message)
            else:
                on_block(message)

        return wrapper if len(banned) > 0 else func

    return decorator

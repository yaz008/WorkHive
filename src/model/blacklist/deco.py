from typing import Callable

from model.blacklist.load import load_blacklist
from model.types import User


def blacklist(
    path: str, on_block: Callable[[User], None] = lambda _: None
) -> Callable[[Callable[[User], None]], Callable[[User], None]]:
    def decorator(func: Callable[[User], None]) -> Callable[[User], None]:
        banned: set[int] = load_blacklist(path=path)

        def wrapper(user: User) -> None:
            if user.telegram_id not in banned:
                func(user)
            else:
                on_block(user)

        return wrapper

    return decorator

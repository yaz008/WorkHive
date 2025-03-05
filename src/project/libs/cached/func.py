from itertools import chain
from typing import Callable, cast, Any


class _Cache:
    __caches: list[dict[tuple[Any, ...], Any]] = list()

    @classmethod
    def register(cls) -> int:
        index: int = len(cls.__caches)
        cls.__caches.append(dict())
        return index

    @classmethod
    def get(
        cls, __index: int, __args: tuple[Any, ...], /
    ) -> dict[tuple[Any, ...], Any] | None:
        return cls.__caches[__index].get(__args)

    @classmethod
    def set(cls, __index: int, __args: tuple[Any, ...], __ret: Any, /) -> None:
        cls.__caches[__index] |= {__args: __ret}


def cache[**Args, Ret](func: Callable[Args, Ret]) -> Callable[Args, Ret]:
    index: int = _Cache.register()

    def wrapper(*args: Args.args, **kwargs: Args.kwargs) -> Ret:
        nonlocal index
        tupled_args: tuple[Any, ...] = tuple(chain(args, kwargs.values()))
        if _Cache.get(index, tupled_args) is None:
            _Cache.set(index, tupled_args, func(*args, **kwargs))
        return cast(Ret, _Cache.get(index, tupled_args))

    return wrapper

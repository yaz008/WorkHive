from typing import Callable

from project.configs import VerboseConfig, VerboseLevel


def print_message(message: str | None) -> None:
    if message is not None:
        print(message)


def compile_renderer(verbose_level: VerboseLevel) -> Callable[[str | None], None]:
    if verbose_level < VerboseConfig.Level:
        return lambda _: None
    return print_message


def verbose[**Args, Ret](
    *,
    before: str | None = None,
    after: str | None = None,
    level: VerboseLevel = VerboseLevel.INFO,
) -> Callable[[Callable[Args, Ret]], Callable[Args, Ret]]:
    def decorator(func: Callable[Args, Ret]) -> Callable[Args, Ret]:
        render: Callable[[str | None], None] = compile_renderer(verbose_level=level)

        def wrapper(*args: Args.args, **kwargs: Args.kwargs) -> Ret:
            render(before)
            result: Ret = func(*args, **kwargs)
            render(after)
            return result

        return wrapper

    return decorator

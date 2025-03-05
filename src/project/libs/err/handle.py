from typing import Callable, Any


def handle_error[Error: Exception, **Args, Ret](
    error: type[Error],
    handler: Callable[[Error, tuple[Any, ...], dict[str, Any]], Ret | None],
) -> Callable[[Callable[Args, Ret]], Callable[Args, Ret | None]]:
    def decorator(func: Callable[Args, Ret]) -> Callable[Args, Ret | None]:
        def wrapper(*args: Args.args, **kwargs: Args.kwargs) -> Ret | None:
            try:
                return func(*args, **kwargs)
            except error as e:
                return handler(e, args, kwargs)

        return wrapper

    return decorator

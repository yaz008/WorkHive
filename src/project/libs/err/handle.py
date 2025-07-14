from typing import Callable


def handle_error[Error: Exception, **Args, Ret](
    error: type[Error],
    routes: dict[Callable[[Error], bool], Callable[Args, Ret]],
) -> Callable[[Callable[Args, Ret]], Callable[Args, Ret]]:
    def decorator(func: Callable[Args, Ret]) -> Callable[Args, Ret]:
        def wrapper(*args: Args.args, **kwargs: Args.kwargs) -> Ret:
            try:
                return func(*args, **kwargs)
            except error as e:
                for filter, handler in routes.items():
                    if filter(e):
                        return handler(*args, **kwargs)
                else:
                    raise e

        return wrapper

    return decorator

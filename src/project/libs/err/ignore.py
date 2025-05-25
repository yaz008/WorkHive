# mypy: disable-error-code="misc"
from typing import Callable, overload

from project.libs.err.exceptions import MutuallyExclusiveArgumentsError
from project.libs.err.logger import exception_logger


@overload
def ignore_error[Error: Exception, **Args, Ret](
    error: type[Error],
) -> Callable[[Callable[Args, Ret]], Callable[Args, Ret | None]]:
    raise NotImplementedError


@overload
def ignore_error[Error: Exception, **Args, Ret](
    error: type[Error], *, default: Ret
) -> Callable[[Callable[Args, Ret]], Callable[Args, Ret]]:
    raise NotImplementedError


@overload
def ignore_error[Error: Exception, **Args, Ret](
    error: type[Error], *, return_error: bool
) -> Callable[[Callable[Args, Ret]], Callable[Args, Ret | Error]]:
    raise NotImplementedError


def ignore_error[Error: Exception, **Args, Ret](
    error: type[Error],
    *,
    default: Ret | None = None,
    return_error: bool = False,
) -> Callable[[Callable[Args, Ret]], Callable[Args, Ret | Error | None]]:
    if default is not None and return_error is True:
        raise MutuallyExclusiveArgumentsError('default', 'return_error')

    def decorator(
        func: Callable[Args, Ret],
    ) -> Callable[Args, Ret | Error | None]:
        def wrapper(*args: Args.args, **kwargs: Args.kwargs) -> Ret | Error | None:
            try:
                return func(*args, **kwargs)
            except error as e:
                exception_logger.write(
                    str(e),
                    **{str(index): str(arg) for index, arg in enumerate(args)}
                    | {name: str(value) for name, value in kwargs.items()},
                )
                return e if return_error else default

        return wrapper

    return decorator

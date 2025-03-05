from typing import Callable, Literal, Any, get_args, get_origin, cast

from project.core.config.exceptions import GetterError, ErrorCode
from project.core.config.manager.types import JSON


def get[T: JSON](
    cfg: dict[str, JSON],
    varname: str,
    vartype: type[T],
    default: T,
    hooks: dict[type, Callable[[JSON], Any]] | None = None,
) -> T:
    new_value: JSON = cfg.get(varname, default)
    if get_origin(vartype) is Literal:
        if new_value not in get_args(vartype):
            raise GetterError(code=ErrorCode.InvalidOptionTypeError)
        return cast(T, new_value)
    if not isinstance(new_value, vartype):
        if hooks is None or vartype not in hooks:
            raise GetterError(code=ErrorCode.InvalidOptionTypeError)
        return cast(T, hooks[vartype](new_value))
    return new_value

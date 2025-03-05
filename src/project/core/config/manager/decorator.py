from typing import Callable, Any

from project.core.config.exceptions import (
    GetterError,
    ErrorCode,
    UnknownOptionsError,
    InvalidOptionTypeError,
)
from project.core.config.manager.getter import get
from project.core.config.manager.load import load_config
from project.core.config.manager.types import JSON


def config[ConfigT](
    filename: str,
    hooks: dict[type, Callable[[JSON], Any]] | None = None,
) -> Callable[[ConfigT], ConfigT]:
    def decorator(cls: ConfigT) -> ConfigT:
        cfg: dict[str, JSON] = load_config(filename)
        unknown_keys: set[str] = cfg.keys() - cls.__annotations__.keys()
        if len(unknown_keys) > 0:
            raise UnknownOptionsError(filename, unknown_keys)
        for varname, vartype in cls.__annotations__.items():
            try:
                new_value: Any = get(
                    cfg=cfg,
                    varname=varname,
                    vartype=vartype,
                    default=getattr(cls, varname),
                    hooks=hooks,
                )
            except GetterError as getter_error:
                match getter_error.code:
                    case ErrorCode.InvalidOptionTypeError:
                        raise InvalidOptionTypeError(filename, varname, vartype)
            setattr(cls, varname, new_value)
        return cls

    return decorator

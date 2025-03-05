from dataclasses import dataclass, field
from typing import Callable, Any

from project.configs import FSAConfig
from project.libs.fsa.exceptions import InvalidMainDelimiterCountError


@dataclass(slots=True)
class FSASerializer:
    unstructure_hooks: dict[type, Callable[[Any], str]] = field(
        default_factory=dict, init=False
    )
    structure_hooks: dict[type, Callable[[str], Any]] = field(
        default_factory=dict, init=False
    )

    def register_unstructure_hook[Arg](
        self, type: type[Arg]
    ) -> Callable[[Callable[[Arg], str]], Callable[[Arg], str]]:
        def decorator(func: Callable[[Arg], str]) -> Callable[[Arg], str]:
            self.unstructure_hooks |= {type: func}
            return func

        return decorator

    def register_structure_hook[Arg](
        self, type: type[Arg]
    ) -> Callable[[Callable[[str], Arg]], Callable[[str], Arg]]:
        def decorator(func: Callable[[str], Arg]) -> Callable[[str], Arg]:
            self.structure_hooks |= {type: func}
            return func

        return decorator

    def serialize(
        self, state: str, symbol: str, args: tuple[Any, ...] | None = None
    ) -> str:
        return FSAConfig.MainDelimiter.join(
            [
                state,
                symbol,
                FSAConfig.ArgDelimiter.join(
                    self.unstructure_hooks.get(type(arg), lambda arg: str(arg))(arg)
                    for arg in (args if args is not None else ())
                ),
            ]
        )

    def deserialize(self, args: str, argtypes: tuple[type, ...], /) -> tuple[Any, ...]:
        return tuple(
            self.structure_hooks.get(argtype, lambda arg: arg)(arg)
            for arg, argtype in zip(
                args.split(sep=FSAConfig.ArgDelimiter), argtypes[2:]
            )
        )

    def unpack(self, __transition_data: str, /) -> tuple[str, str, str]:
        match __transition_data.count(FSAConfig.MainDelimiter):
            case 1:
                state, symbol = __transition_data.split(
                    sep=FSAConfig.MainDelimiter, maxsplit=1
                )
                return (state, symbol, str())
            case 2:
                state, symbol, args = __transition_data.split(
                    sep=FSAConfig.MainDelimiter, maxsplit=2
                )
                return (state, symbol, args)
            case _:
                raise InvalidMainDelimiterCountError(__transition_data)

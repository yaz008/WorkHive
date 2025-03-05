from dataclasses import dataclass, field, asdict
from typing import Callable, Any, cast
from uuid import UUID, uuid4

from project.libs.cached import cache
from project.libs.tgdraw.types.info.load import load_button


@dataclass(slots=True, unsafe_hash=True)
class ButtonInfo:
    text: str
    data: str

    def __iter__(self):
        return iter([self.text, self.data])

    @property
    def asdict(self) -> dict[str, str]:
        return cast(dict[str, str], asdict(self))


@dataclass(slots=True, unsafe_hash=True)
class LoadInfo:
    name: str
    language: str


@dataclass(slots=True)
class ButtonFactory:
    serialize: Callable[[str, str, tuple[Any, ...] | None], str]
    saved_buttons: dict[str, str] = field(default_factory=dict, init=False)
    __cache_id__: UUID = field(init=False)

    def __post_init__(self) -> None:
        self.__cache_id__ = uuid4()

    def __hash__(self) -> int:
        return hash(self.__cache_id__)

    def __eq__(self, __other: object, /) -> bool:
        return cast(bool, self.__cache_id__ == getattr(__other, '__cache_id__'))

    @cache
    def create(
        self,
        state: str,
        symbol: str,
        info: str | LoadInfo,
        args: tuple[Any, ...] | None = None,
    ) -> ButtonInfo:
        return ButtonInfo(
            text=(
                info if isinstance(info, str) else load_button(info.name, info.language)
            ),
            data=self.serialize(state, symbol, args),
        )

    def save(self, name: str, symbol: str) -> None:
        self.saved_buttons |= {name: symbol}


@dataclass(slots=True)
class ButtonFactoryClosure:
    state: str
    language: str
    factory: ButtonFactory

    def create(
        self,
        symbol: str,
        name: str,
        args: tuple[Any, ...] | None = None,
        load: bool = True,
    ) -> ButtonInfo:
        return self.factory.create(
            state=self.state,
            symbol=symbol,
            info=LoadInfo(name=name, language=self.language) if load else name,
            args=args,
        )

    def saved(
        self,
        name: str,
        args: tuple[Any, ...] | None = None,
    ) -> ButtonInfo:
        return self.create(
            symbol=self.factory.saved_buttons[name],
            name=name,
            args=args,
        )

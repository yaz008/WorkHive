from dataclasses import dataclass, field, asdict
from typing import Callable, Any, cast

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


@dataclass(slots=True)
class LoadInfo:
    name: str
    language: str


@dataclass(slots=True)
class ButtonFactory:
    serialize: Callable[[str, str, tuple[Any, ...] | None], str]
    saved_buttons: dict[str, str] = field(default_factory=dict, init=False)

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

    def saved(self, name: str) -> ButtonInfo:
        return self.create(
            symbol=self.factory.saved_buttons[name],
            name=name,
        )

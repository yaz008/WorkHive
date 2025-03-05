from dataclasses import dataclass
from typing import Callable, Protocol


class HasName(Protocol):
    name: str


class HasState(Protocol):
    state: str


@dataclass(slots=True)
class State[Stateful: HasState, Ret]:
    name: str
    transitions: dict[str, str]
    action: Callable[[Stateful, str], Ret]

    def __eq__(self, __other: object) -> bool:
        return (
            __other.__class__.__name__ == self.__class__.__name__
            and hasattr(__other, 'name')
            and self.name == __other.__dict__['name']
        )

from dataclasses import dataclass, field
from inspect import signature
from typing import Callable, Protocol, cast

from project.configs import FSAState, FSASymbol
from project.libs.fsa.exceptions import (
    InvalidTransitionError,
    UnexpectedStateError,
    DuplicateStateError,
    StartNotCommonError,
    InitialStateTransitionError,
)
from project.libs.fsa.imports import import_all
from project.libs.fsa.router.content import TGContentType
from project.libs.fsa.router.state import State, HasState
from project.libs.fsa.serializer import serializer
from project.libs.tgdraw import ButtonFactory, ButtonFactoryClosure


class UserProtocol(HasState, Protocol):
    language: str


@dataclass(slots=True)
class FSA[User: UserProtocol, Ret]:
    routs: str
    button_factory: ButtonFactory
    initial_transition_state: str
    common_transitions: dict[str, dict[str, str]]
    __states: dict[str, State[User, Ret]] = field(default_factory=dict, init=False)
    __acceptance_table: dict[str, frozenset[TGContentType]] = field(
        default_factory=dict, init=False
    )

    def __post_init__(self) -> None:
        if not all(
            FSASymbol.Start in transitions
            for transitions in self.common_transitions.values()
        ):
            raise StartNotCommonError
        self.__states |= {
            FSAState.Initial: State(
                name=FSAState.Initial,
                transitions={FSASymbol.Start: self.initial_transition_state},
                action=cast(Callable[[User, str], Ret], ()),
            )
        }

    def shift(self, __user: User, __transition_data: str, /) -> Ret:
        expected_state, symbol, args = serializer.unpack(__transition_data)
        if expected_state != __user.state:
            raise UnexpectedStateError(expected_state, __user.state)
        state: State = self.__states[__user.state]
        if symbol in state.transitions:
            new_state: State = self.__states[state.transitions[symbol]]
            __user.state = new_state.name
            return cast(Ret, new_state.action(__user, args))
        raise InvalidTransitionError(state.name, symbol)

    def add(
        self,
        name: str,
        pipeline: str,
        transitions: dict[str, str] | None = None,
        accepts_types: tuple[TGContentType, ...] | None = None,
    ) -> Callable[[Callable[..., Ret]], None]:
        def decorator(func: Callable[..., Ret]) -> None:
            if name in self.__states:
                raise DuplicateStateError(name)
            if transitions is not None:
                for symbol, state in transitions.items():
                    if state == FSAState.Initial:
                        raise InitialStateTransitionError(name, symbol)
            argtypes: tuple[type, ...] = tuple(
                argtype.annotation for argtype in signature(func).parameters.values()
            )

            def action(__user: User, __args: str, /) -> Ret:
                return func(
                    __user,
                    ButtonFactoryClosure(
                        state=__user.state,
                        language=__user.language,
                        factory=self.button_factory,
                    ),
                    *serializer.deserialize(__args, argtypes),
                )

            self.__acceptance_table |= {
                name: frozenset(accepts_types if accepts_types is not None else ())
            }
            self.__states |= {
                name: State(
                    name=name,
                    transitions=(transitions if transitions is not None else {})
                    | self.common_transitions[pipeline],
                    action=action,
                )
            }

        return decorator

    def connect(self) -> None:
        import_all(self.routs)
        assert self.is_connected

    def accepts(self, state: str, content_type: TGContentType) -> bool:
        return content_type in self.__acceptance_table[state]

    @property
    def is_connected(self) -> bool:
        visited: set[str] = set()
        stack: list[str] = [FSAState.Initial]

        while len(stack) != 0:
            current_vertex: str = stack.pop()
            if current_vertex not in visited:
                visited.add(current_vertex)
                current_state: State = self.__states[current_vertex]
                for neighbor in current_state.transitions.values():
                    if neighbor not in visited:
                        stack.append(neighbor)
        return len(visited) == len(self.__states)

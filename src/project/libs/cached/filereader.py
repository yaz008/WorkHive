from dataclasses import dataclass, field
from typing import Literal, overload, cast, Protocol


class HasRead(Protocol):
    def read(self) -> str | bytes:
        raise NotImplementedError


@dataclass(slots=True)
class CachedFileReader:
    __cache: dict[str, str | bytes] = field(default_factory=dict, init=False)

    @overload
    def read(self, path: str, mode: Literal['r']) -> str:
        raise NotImplementedError

    @overload
    def read(self, path: str, mode: Literal['rb']) -> bytes:
        raise NotImplementedError

    def read(self, path: str, mode: Literal['r', 'rb']) -> str | bytes:
        if path not in self.__cache.keys():
            kwargs: dict[str, str] = {
                'file': path,
                'mode': mode,
            }
            if mode == 'r':
                kwargs |= {'encoding': 'UTF-8'}
            with open(**kwargs) as file_reader:  # type: ignore[call-overload]
                self.__cache |= {path: cast(HasRead, file_reader).read()}
        return self.__cache[path]

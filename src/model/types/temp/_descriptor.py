from dataclasses import dataclass
from typing import Protocol, Any


class HasDct(Protocol):
    dct: dict[str, Any]


@dataclass(slots=True)
class TempDescriptor:
    attrname: str

    def __get__(self, obj: HasDct, _: type | None = None) -> Any | None:
        return obj.dct.get(self.attrname)

    def __set__(self, obj: HasDct, new: Any) -> None:
        obj.dct |= {self.attrname: new}

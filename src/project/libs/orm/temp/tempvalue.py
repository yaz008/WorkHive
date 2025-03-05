from dataclasses import dataclass, field


class _TempValue(dict):
    pass


@dataclass
class TempValue:
    value: _TempValue = field(default_factory=_TempValue)

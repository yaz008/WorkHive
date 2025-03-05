from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType


def import_all(base_fodler: str) -> None:
    package: ModuleType = import_module(base_fodler)
    for info in iter_modules(path=package.__path__, prefix=f'{package.__name__}.'):
        import_module(info.name)
        if info.ispkg:
            import_all(info.name)

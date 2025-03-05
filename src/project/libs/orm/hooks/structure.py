from datetime import datetime
from json import loads
from uuid import UUID

from cattrs import Converter

from project.libs.orm.temp import _TempValue


converter: Converter = Converter()

converter.register_structure_hook(
    datetime, lambda value, _: datetime.fromisoformat(value)
)
converter.register_structure_hook(UUID, lambda value, _: UUID(value))
converter.register_structure_hook(_TempValue, lambda value, _: _TempValue(loads(value)))

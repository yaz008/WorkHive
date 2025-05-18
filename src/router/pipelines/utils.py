from model.tables import _Metadata, metadata_table
from model.types import User


def in_metadata(user: User, value: str) -> bool:
    return value in [m.value for m in user.metadata.values()]


def add_metadata(user: User, value: str) -> None:
    metadata_table.update({user.workhive_id: _Metadata(value=value)})

from dataclasses import dataclass, field
from datetime import datetime

from project.configs import SessionConfig


@dataclass
class Session:
    telegram_id: int
    message_id: int
    kind: str
    sending_time: datetime = field(init=False)
    last_accessed: datetime = field(init=False)

    def __post_init__(self) -> None:
        self.sending_time = datetime.now()
        self.last_accessed = self.sending_time

    @property
    def is_valid(self) -> bool:
        return datetime.now() > self.expiration_time

    @property
    def expiration_time(self) -> datetime:
        return self.sending_time + SessionConfig.MaxLifeTime

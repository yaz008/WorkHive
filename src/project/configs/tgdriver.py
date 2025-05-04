from typing import Literal

from project.core.config import config


TGParseMode = Literal['HTML', 'Markdown', 'MarkdownV2']


@config(filename='tg-driver')
class TGDriverConfig:
    DefaultParseMode: TGParseMode = 'HTML'
    SkipPending: bool = True
    Threads: int = 1
    IsThreaded: bool = False
    OnBotStart: str = 'Bot started'

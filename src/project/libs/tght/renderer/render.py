from typing import Callable

from project.configs import TGDriverConfig, TGParseMode
from project.libs.tght.reader import file_reader
from project.libs.tght.renderer.html import render_html


def render(
    text: str,
    tag_handlers: dict[str, Callable[[str], str]] | None = None,
    parse_mode: TGParseMode = TGDriverConfig.DefaultParseMode,
) -> str:
    match parse_mode:
        case 'HTML':
            return render_html(
                text=text, tag_handlers=tag_handlers if tag_handlers is not None else {}
            )
        case _:
            raise NotImplementedError


def render_file(
    language: str,
    state: str,
    tag_handlers: dict[str, Callable[[str], str]] | None = None,
    parse_mode: TGParseMode = TGDriverConfig.DefaultParseMode,
) -> str:
    return render(
        text=file_reader.read(language=language, state=state),
        tag_handlers=tag_handlers if tag_handlers is not None else {},
        parse_mode=parse_mode,
    )

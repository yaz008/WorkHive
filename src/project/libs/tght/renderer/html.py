from dataclasses import dataclass
from re import Pattern, compile, finditer, split, DOTALL
from typing import Callable


@dataclass(slots=True)
class Tag:
    name: str
    content: str


class CompiledPattern:
    FindTags: Pattern = compile(r'<([\w\d_-]+)>(.*?)</\1>', DOTALL)
    FindPlain: Pattern = compile(r'<(?:[\w\d_-]+)>.*?</(?:[\w\d_-]+)>', DOTALL)


def get_tags(text: str) -> tuple[Tag, ...]:
    return tuple(
        Tag(name=m.group(1), content=m.group(2))
        for m in finditer(CompiledPattern.FindTags, text)
    )


def get_plain(text: str) -> tuple[str, ...]:
    return tuple(plain for plain in split(CompiledPattern.FindPlain, text))


def render_html(text: str, tag_handlers: dict[str, Callable[[str], str]]) -> str:
    processed_tags, plain_parts = tuple(
        tag_handlers.get(
            tag.name, lambda content: f'<{tag.name}>{content}</{tag.name}>'
        )(tag.content)
        for tag in get_tags(text)
    ), get_plain(text)
    result: str = plain_parts[0]
    for i in range(1, len(processed_tags) + len(plain_parts)):
        result += (plain_parts if i % 2 == 0 else processed_tags)[i // 2]
    return result

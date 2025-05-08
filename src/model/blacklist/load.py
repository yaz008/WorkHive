from json import load
from typing import cast


def load_blacklist(path: str) -> set[int]:
    try:
        with open(file=path, mode='r', encoding='UTF-8') as blacklist_file:
            return cast(set[int], load(blacklist_file))
    finally:
        return set()

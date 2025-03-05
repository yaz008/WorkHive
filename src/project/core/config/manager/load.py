from json import loads
from os import listdir
from typing import cast

from project.core.config.exceptions import EmptyConfigFileError
from project.core.config.manager.types import JSON


def load_config(filename: str) -> dict[str, JSON]:
    if f'{filename}.json' not in listdir('configs'):
        return dict()
    with open(
        file=f'configs\\{filename}.json', mode='r', encoding='UTF-8'
    ) as config_file:
        content: str = config_file.read()
        if len(content.strip()) == 0:
            raise EmptyConfigFileError(filename)
        return cast(dict[str, JSON], loads(content))

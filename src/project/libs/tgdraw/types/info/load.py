from json import load
from typing import cast

from project.configs import ButtonConfig
from project.libs.cached import cache


@cache
def load_button(name: str, language: str) -> str:
    with open(
        file=f'{ButtonConfig.ButtonsFolder}\\{name}.json',
        mode='r',
        encoding='UTF-8',
    ) as button_info:
        return cast(str, load(button_info)[language])

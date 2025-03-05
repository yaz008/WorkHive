from itertools import chain
from typing import Generator, Iterable, Callable

from telebot.types import InlineKeyboardMarkup

from project.configs import ButtonConfig
from project.libs.cached import cache
from project.libs.tgdraw.types import TGKeyboard, InlineTGButton, ButtonInfo


@cache
def options_generator(
    options: tuple[ButtonInfo, ...], is_checked: Callable[[int], bool]
) -> Generator[InlineTGButton, None, None]:
    return (
        InlineTGButton(
            text=ButtonConfig.CheckDelimiter.join(
                chain(
                    (ButtonConfig.Checked,) if is_checked(index) else (),
                    (option.text,),
                )
            ),
            data=option.data,
        )
        for index, option in enumerate(options)
    )


@cache
def optional_next(
    buttons: Iterable[InlineTGButton],
    layout: tuple[int, ...],
    next: ButtonInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return TGKeyboard(
        buttons=tuple(
            chain(
                buttons,
                (
                    (
                        InlineTGButton(
                            text=next.text,
                            data=next.data,
                        ),
                    )
                    if next is not None
                    else ()
                ),
            )
        ),
        layout=tuple(chain(layout, (1 if next is not None else 0,))),
        cls=InlineKeyboardMarkup,
    )

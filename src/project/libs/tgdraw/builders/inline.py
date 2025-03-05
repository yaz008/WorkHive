from itertools import chain

from telebot.types import InlineKeyboardMarkup

from project.libs.cached import cache
from project.libs.tgdraw.builders.generators import options_generator, optional_next
from project.libs.tgdraw.types import (
    TGKeyboard,
    InlineTGButton,
    ButtonInfo,
    ButtonFactoryClosure,
)


@cache
def keyboard(
    buttons: tuple[ButtonInfo, ...],
    layout: tuple[int, ...],
    next: ButtonInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return optional_next(
        buttons=tuple(
            InlineTGButton(
                text=button_info.text,
                data=button_info.data,
            )
            for button_info in buttons
        ),
        layout=layout,
        next=next,
    )


@cache
def choice(
    options: tuple[ButtonInfo, ...], checked: int, next: ButtonInfo | None = None
) -> TGKeyboard[InlineKeyboardMarkup]:
    return optional_next(
        buttons=options_generator(options, lambda index: index == checked),
        layout=tuple(1 for _ in range(len(options))),
        next=next,
    )


@cache
def checklist(
    options: tuple[ButtonInfo, ...],
    flags: tuple[bool, ...],
    next: ButtonInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return optional_next(
        buttons=options_generator(options, lambda index: flags[index]),
        layout=tuple(1 for _ in range(len(options))),
        next=next,
    )


@cache
def numeric(
    factory: ButtonFactoryClosure,
    symbol: str,
    back: ButtonInfo,
    next: ButtonInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return optional_next(
        buttons=chain(
            (
                InlineTGButton(
                    **factory.create(
                        symbol=symbol, name=str(n), load=False, args=(n,)
                    ).asdict
                )
                for n in range(1, 10)
            ),
            (
                InlineTGButton(text=back.text, data=back.data),
                InlineTGButton(
                    **factory.create(
                        symbol=symbol, name='0', load=False, args=(0,)
                    ).asdict
                ),
                InlineTGButton(
                    **factory.create(
                        symbol=symbol, name='⌫', load=False, args=('<',)
                    ).asdict
                ),
            ),
        ),
        layout=(3, 3, 3, 3),
        next=next,
    )

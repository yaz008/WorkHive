from itertools import chain

from telebot.types import InlineKeyboardMarkup

from project.libs.cached import cache
from project.libs.tgdraw.types import (
    TGKeyboard,
    ButtonInfo,
    KeyboardInfo,
    ButtonFactoryClosure,
)


@cache
def keyboard(
    keyboard: KeyboardInfo,
    optional_keyboard: KeyboardInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return TGKeyboard(
        buttons=tuple(
            chain(
                keyboard.render(),
                optional_keyboard.render() if optional_keyboard is not None else (),
            )
        ),
        layout=tuple(
            chain(
                keyboard.layout,
                optional_keyboard.layout if optional_keyboard is not None else (),
            )
        ),
        cls=InlineKeyboardMarkup,
    )


@cache
def choice(
    options: tuple[ButtonInfo, ...],
    checked: int | None = None,
    optional_keyboard: KeyboardInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return keyboard(
        keyboard=KeyboardInfo(
            buttons=options,
            layout=tuple(1 for _ in range(len(options))),
            is_checked=lambda index: index == checked,
        ),
        optional_keyboard=optional_keyboard,
    )


@cache
def checklist(
    options: tuple[ButtonInfo, ...],
    flags: tuple[bool, ...],
    optional_keyboard: KeyboardInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return keyboard(
        keyboard=KeyboardInfo(
            buttons=options,
            layout=tuple(1 for _ in range(len(options))),
            is_checked=lambda index: flags[index],
        ),
        optional_keyboard=optional_keyboard,
    )


@cache
def numeric(
    factory: ButtonFactoryClosure,
    symbol: str,
    back: ButtonInfo,
    next: ButtonInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return keyboard(
        keyboard=(
            KeyboardInfo(
                buttons=tuple(
                    chain(
                        (
                            factory.create(
                                symbol=symbol, name=str(n), args=(n,), load=False
                            )
                            for n in range(1, 10)
                        ),
                        (
                            back,
                            factory.create(
                                symbol=symbol, name='0', load=False, args=(0,)
                            ),
                            factory.create(
                                symbol=symbol, name='⌫', load=False, args=('<',)
                            ),
                        ),
                    )
                ),
                layout=(3, 3, 3, 3),
            )
            if next is None
            else KeyboardInfo(
                buttons=(
                    back,
                    next,
                    factory.create(symbol=symbol, name='⌫', load=False, args=('<',)),
                ),
                layout=(3,),
            )
        )
    )

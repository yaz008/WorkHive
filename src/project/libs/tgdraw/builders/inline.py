from itertools import chain

from telebot.types import InlineKeyboardMarkup

from project.configs import ButtonConfig
from project.libs.cached import cache
from project.libs.tgdraw.types import (
    TGKeyboard,
    ButtonInfo,
    RowInfo,
    ButtonFactoryClosure,
)


@cache
def keyboard(
    *rows: RowInfo | None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return TGKeyboard(
        buttons=tuple(chain(*(row.render() for row in rows if row is not None))),
        layout=tuple(
            len(tuple(filter(lambda button: button is not None, row.buttons)))
            for row in rows
            if row is not None
        ),
        cls=InlineKeyboardMarkup,
    )


@cache
def choice(
    options: tuple[ButtonInfo, ...],
    checked: int | None = None,
    *rows: RowInfo,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return keyboard(
        *(
            RowInfo(
                ButtonInfo(
                    text=ButtonConfig.CheckDelimiter.join(
                        chain(
                            (ButtonConfig.Checked,) if index == checked else (),
                            (option.text,),
                        )
                    ),
                    data=option.data,
                )
            )
            for index, option in enumerate(options)
        ),
        *rows,
    )


@cache
def numeric(
    factory: ButtonFactoryClosure,
    symbol: str,
    back: ButtonInfo,
    next: ButtonInfo | None = None,
) -> TGKeyboard[InlineKeyboardMarkup]:
    return keyboard(
        *(
            chain(
                (
                    RowInfo(
                        *(
                            factory.create(
                                symbol=symbol,
                                name=str(k + 1),
                                args=(k + 1,),
                                load=False,
                            )
                            for k in range(3 * n, 3 * (n + 1))
                        )
                    )
                    for n in range(3)
                ),
                (
                    RowInfo(
                        back,
                        factory.create(symbol=symbol, name='0', load=False, args=(0,)),
                        factory.create(
                            symbol=symbol, name='⌫', load=False, args=('<',)
                        ),
                    ),
                ),
            )
            if next is None
            else (
                RowInfo(
                    back,
                    next,
                    factory.create(symbol=symbol, name='⌫', load=False, args=('<',)),
                ),
            )
        )
    )

from typing import cast

from telebot.types import Message, CallbackQuery

from driver import driver
from model.blacklist import blacklist
from model.deco import delete_message, register, with_user
from model.types import User, TempUser
from project.configs import FSASymbol
from project.libs.fsa import serializer
from project.libs.tgdraw import TGMessage
from router import router


@driver.message_handler(commands=['start'])
@blacklist
@delete_message
@register
def on_start(user: User | TempUser) -> None:
    response: TGMessage = router.shift(
        user,
        serializer.serialize(
            state=user.state,
            symbol=FSASymbol.Start,
            args=(user.language,),
        ),
    )
    driver.update(telegram_id=user.telegram_id, message=response)


@driver.message_handler(content_types=['text'])
@blacklist
@delete_message
@with_user
def on_text(user: User | TempUser, message: Message) -> None:
    if router.accepts(user.state, 'text'):
        response: TGMessage = router.shift(
            user,
            serializer.serialize(
                state=user.state, symbol=FSASymbol.InputData, args=(message.text,)
            ),
        )
        driver.update(telegram_id=user.telegram_id, message=response)


@driver.callback_query_handler(func=None)
@with_user
def on_callback(user: User | TempUser, callback: CallbackQuery) -> None:
    response: TGMessage = router.shift(user, cast(str, callback.data))
    driver.update(telegram_id=user.telegram_id, message=response)


@driver.message_handler(
    content_types=[
        'text',
        'photo',
        'audio',
        'document',
        'video',
        'video_note',
        'voice',
        'sticker',
        'location',
        'contact',
        'poll',
    ]
)
@blacklist
@delete_message
def _(_: Message) -> None:
    pass


if __name__ == '__main__':
    router.connect()
    driver.infinity_polling()

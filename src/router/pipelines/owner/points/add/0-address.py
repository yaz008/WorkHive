from re import findall

from telebot.types import LinkPreviewOptions

from model.tables import temp_points
from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.orm import TempValue
from project.libs.tgdraw import (
    TGMedia,
    TGMessage,
    ButtonFactoryClosure,
    RowInfo,
    keyboard,
)
from project.libs.tght import render_file
from router.instance import router
from router.loggers import address_logger


def get_temp_point(telegram_id: int) -> TempPoint:
    id_in_keys: bool = telegram_id in temp_points.keys
    if not id_in_keys:
        temp_points.update({telegram_id: TempValue()})
    return TempPoint(telegram_id, set_default=(not id_in_keys))


def get_link(string: str) -> str | None:
    links: list[str] = findall(
        pattern=r'https://[\w=$%&?#@!\/\+\-\*\.]+',
        string=string,
    )
    return links[0] if len(links) > 0 else None


@router.add(
    name=FSAState.OwnerPointAddress,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPoints,
        FSASymbol.InputData: FSAState.OwnerPointAddress,
        FSASymbol.Next: FSAState.OwnerPointPayload,
    },
    accepts_types=('text',),
)
def owner_point_address(
    owner: Owner, factory: ButtonFactoryClosure, share_info: str
) -> TGMessage:
    if share_info != str():
        address_logger.write(message=share_info)
    point: TempPoint = get_temp_point(owner.telegram_id)
    link: str | None = get_link(share_info)
    if link is not None:
        point.yandex_link = link
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'link': lambda placeholder: (
                    point.yandex_link if point.yandex_link is not None else placeholder
                ),
                'payload': lambda _: str(point.payload),
                'minimal-charge': lambda _: str(point.minimal_charge),
                'charge-per-one': lambda _: (
                    f'{point.charge_per_one // 100}.{(
                            '0' if point.charge_per_one % 100 < 10 else str()
                        )}{point.charge_per_one % 100}'
                ),
                'name': lambda placeholder: f'<code>{(
                    point.name if point.name != str() else placeholder
                )}</code>',
                'on-error': lambda _: (
                    render_file(
                        language=owner.language, state='owner-point-address-error'
                    )
                    if link is None and share_info != str()
                    else str()
                ),
            },
        ),
        tgmedia=(
            TGMedia(
                name='share-instruction',
                kind='Photo',
                language=owner.language,
            )
            if point.address == str()
            else None
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(WorkHiveButton.Back),
                (
                    factory.saved(WorkHiveButton.Next)
                    if point.yandex_link != str()
                    else None
                ),
            ),
        ),
        link_preview=(
            LinkPreviewOptions(
                url=point.yandex_link, prefer_small_media=True, show_above_text=True
            )
            if point.yandex_link != str()
            else None
        ),
    )

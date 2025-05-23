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


def get_temp_point(telegram_id: int) -> TempPoint:
    id_in_keys: bool = telegram_id in temp_points.keys
    if not id_in_keys:
        temp_points.update({telegram_id: TempValue()})
    return TempPoint(telegram_id, set_default=(not id_in_keys))


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
    point: TempPoint = get_temp_point(owner.telegram_id)
    is_error: bool = False
    if share_info != str():
        try:
            point.franchise, point.address, point.yandex_link = share_info.split(
                sep='\n', maxsplit=2
            )
        except ValueError:
            is_error = True
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'address': lambda placeholder: (
                    f'<a href=\"{point.yandex_link}\">{point.address}</a>'
                    if point.address != str()
                    else f'<code>{placeholder}</code>'
                ),
                'payload': lambda _: str(point.payload),
                'minimal-charge': lambda _: str(point.minimal_charge),
                'charge-per-one': lambda _: (
                    f'{point.charge_per_one // 100}.{point.charge_per_one % 100}'
                ),
                'name': lambda placeholder: f'<code>{(
                    point.name if point.name != str() else placeholder
                )}</code>',
                'on-error': lambda _: (
                    render_file(
                        language=owner.language, state='owner-point-address-error'
                    )
                    if is_error
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
                factory.saved(WorkHiveButton.Next) if point.address != str() else None,
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

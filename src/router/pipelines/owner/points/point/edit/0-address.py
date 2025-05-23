from re import match
from uuid import UUID

from telebot.types import LinkPreviewOptions

from model.tables import temp_points, _Point
from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.orm import TempValue
from project.libs.orm.temp import _TempValue
from project.libs.tgdraw import (
    TGMessage,
    TGMedia,
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


def create_temp_point(owner: Owner, point_id: UUID) -> None:
    point: _Point = owner.points[point_id]
    temp_points.update(
        {
            owner.telegram_id: TempValue(
                value=_TempValue(
                    {
                        'franchise': point.franchise,
                        'address': point.address,
                        'yandex_link': point.yandex_link,
                        'name': point.name,
                        'payload': point.payload,
                        'minimal_charge': point.minimal_charge,
                        'charge_per_one': point.charge_per_one,
                        'point_id': str(point_id),
                    }
                )
            )
        }
    )


@router.add(
    name=FSAState.OwnerPointAddressEdit,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.InputData: FSAState.OwnerPointAddressEdit,
        FSASymbol.Next: FSAState.OwnerPointPayloadEdit,
        FSASymbol.Back: FSAState.OwnerPoint,
    },
    accepts_types=('text',),
)
def owner_point_address(
    owner: Owner, factory: ButtonFactoryClosure, point_id: str, share_info: str
) -> TGMessage:
    create_temp_point(owner, UUID(point_id))
    point: TempPoint = get_temp_point(owner.telegram_id)
    is_error: bool = False
    if share_info != str():
        try:
            point.franchise, point.address, point.yandex_link = share_info.split(
                sep='\n', maxsplit=2
            )
            if not all(
                [
                    point.franchise.lower().replace('.', ' ')
                    in ('wildberries', 'ozon', 'яндекс маркет', 'yandex market'),
                    match(
                        pattern=r'(?:[А-Я][а-я]+), [а-яА-Я0-9\., ]+',
                        string=point.address,
                    ),
                    match(
                        pattern=r'https://yandex.com/maps/[\w_/=?:\.]+',
                        string=point.yandex_link,
                    ),
                ]
            ):
                raise ValueError
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
                factory.saved(
                    WorkHiveButton.Back,
                    args=(
                        list(owner.points.values()).index(owner.points[UUID(point_id)]),
                        False,
                    ),
                ),
                factory.saved(WorkHiveButton.Next) if point.address != str() else None,
            ),
        ),
        link_preview=LinkPreviewOptions(prefer_small_media=True, show_above_text=True),
    )

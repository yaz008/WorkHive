from re import match
from uuid import UUID

from telebot.types import LinkPreviewOptions

from model.tables import temp_points, _Point
from model.types import Owner, TempPoint
from model.utils import with_yandex_language
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.orm import TempValue
from project.libs.orm.temp import _TempValue
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
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
    name=FSAState.OwnerPointPayloadEdit,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPoint,
        FSASymbol.InputData: FSAState.OwnerPointPayloadEdit,
        FSASymbol.Next: FSAState.OwnerPointChargeEdit,
    },
    accepts_types=('text',),
)
def owner_point_payload(
    owner: Owner, factory: ButtonFactoryClosure, point_id: str, payload: str
) -> TGMessage:
    create_temp_point(owner, UUID(point_id))
    point: TempPoint = get_temp_point(owner.telegram_id)
    if match(pattern=r'[\d]+', string=payload):
        point.payload = int(payload)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'link': lambda placeholder: (
                    with_yandex_language(
                        link=point.yandex_link,
                        language_code=owner.language,
                    )
                    if point.yandex_link is not None
                    else placeholder
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
            },
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
                factory.saved(WorkHiveButton.Next),
            ),
        ),
        link_preview=LinkPreviewOptions(is_disabled=True),
    )

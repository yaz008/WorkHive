from re import match

from telebot.types import LinkPreviewOptions

from model.types import Owner, TempPoint
from model.utils import with_yandex_language
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPointChargeEdit,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPointPayloadEdit,
        FSASymbol.InputData: FSAState.OwnerPointChargeEdit,
        FSASymbol.Next: FSAState.OwnerPointChargePerOneEdit,
    },
    accepts_types=('text',),
)
def owner_point_charge(
    owner: Owner, factory: ButtonFactoryClosure, charge: str
) -> TGMessage:
    point: TempPoint = TempPoint(owner.telegram_id)
    if match(pattern=r'[\d]+', string=charge):
        point.minimal_charge = int(charge)
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
                factory.saved(WorkHiveButton.Back), factory.saved(WorkHiveButton.Next)
            ),
        ),
        link_preview=LinkPreviewOptions(is_disabled=True),
    )

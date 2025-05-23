from re import match

from telebot.types import LinkPreviewOptions

from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPointChargePerOneEdit,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPointChargeEdit,
        FSASymbol.InputData: FSAState.OwnerPointChargePerOneEdit,
        FSASymbol.Next: FSAState.OwnerPointNameEdit,
    },
    accepts_types=('text',),
)
def owner_point_charge_per_one(
    owner: Owner, factory: ButtonFactoryClosure, charge: str
) -> TGMessage:
    point: TempPoint = TempPoint(owner.telegram_id)
    if match(pattern=r'^\d+(?:\.\d\d?)?$', string=charge):
        if '.' in charge:
            rub, fr = charge.split(sep='.', maxsplit=1)
            point.charge_per_one = int(rub) * 100 + int(
                fr if len(fr) == 2 else f'{fr}0'
            )
        else:
            point.charge_per_one = int(charge) * 100
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'address': lambda _: (
                    f'<a href=\"{point.yandex_link}\">{point.address}</a>'
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

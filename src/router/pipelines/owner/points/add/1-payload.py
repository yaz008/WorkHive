from re import match

from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPointPayload,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPointAddress,
        FSASymbol.InputData: FSAState.OwnerPointPayload,
        FSASymbol.Next: FSAState.OwnerPointCharge,
    },
    accepts_types=('text',),
)
def owner_point_payload(
    owner: Owner, factory: ButtonFactoryClosure, payload: str
) -> TGMessage:
    point: TempPoint = TempPoint(owner.telegram_id)
    if match(pattern=r'[\d]+', string=payload):
        point.payload = int(payload)
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
                'charge-per-one': lambda _: str(point.charge_per_one),
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
    )

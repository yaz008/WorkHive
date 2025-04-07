from model.tables import temp_points
from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.orm import TempValue
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
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
    owner: Owner, factory: ButtonFactoryClosure, address: str
) -> TGMessage:
    point: TempPoint = get_temp_point(owner.telegram_id)
    if address != str():
        point.address = address
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'address': lambda default: address if address != str() else default
            },
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Back)),
            RowInfo(factory.saved(WorkHiveButton.Next)) if address != str() else None,
        ),
    )

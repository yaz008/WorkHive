from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPointChargePerOne,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPointCharge,
        FSASymbol.InputData: FSAState.OwnerPointChargePerOne,
        FSASymbol.Next: FSAState.OwnerPointName,
    },
    accepts_types=('text',),
)
def owner_point_charge(
    owner: Owner, factory: ButtonFactoryClosure, charge: str
) -> TGMessage:
    point: TempPoint = TempPoint(owner.telegram_id)
    if charge != str():
        point.charge_per_one = int(charge)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'number': lambda default: charge if charge != str() else default
            },
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Back)),
            RowInfo(factory.saved(WorkHiveButton.Next)) if charge != str() else None,
        ),
    )

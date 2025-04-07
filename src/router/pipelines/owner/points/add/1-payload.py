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
    if payload != str():
        point.payload = int(payload)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'number': lambda default: payload if payload != str() else default
            },
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Back)),
            RowInfo(factory.saved(WorkHiveButton.Next)) if payload != str() else None,
        ),
    )

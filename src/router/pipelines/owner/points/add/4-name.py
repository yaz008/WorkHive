from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPointName,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPointCharge,
        FSASymbol.InputData: FSAState.OwnerPointName,
        FSASymbol.Next: FSAState.OwnerPointDone,
    },
    accepts_types=('text',),
)
def owner_point_name(
    owner: Owner, factory: ButtonFactoryClosure, name: str
) -> TGMessage:
    point: TempPoint = TempPoint(owner.telegram_id)
    if name != str():
        point.name = name
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={'name': lambda default: name if name != str() else default},
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Back)),
            RowInfo(factory.saved(WorkHiveButton.Next)) if name != str() else None,
        ),
    )

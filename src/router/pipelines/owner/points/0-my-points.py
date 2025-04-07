from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPoints,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerMainMenu,
        FSASymbol.Add: FSAState.OwnerPointAddress,
        FSASymbol.Delete: FSAState.OwnerPointDelete,
    },
)
def owner_settings(owner: Owner, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'points': lambda default: (
                    '\n'.join(
                        f'{index}: {point.name}'
                        for index, point in enumerate(owner.points.values(), start=1)
                    )
                    if len(owner.points) > 0
                    else default
                ),
            },
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Add)),
            RowInfo(factory.saved(WorkHiveButton.Delete)),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

from model.tables import points_table
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPointDelete,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerPoints,
        FSASymbol.Delete: FSAState.OwnerPointDelete,
    },
)
def owner_point_payload(
    owner: Owner, factory: ButtonFactoryClosure, index: str
) -> TGMessage:
    if index != str():
        points_table.remove_one(
            owner.workhive_id, list(owner.points.values())[int(index)].__sql_id__
        )
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
        ),
        keyboard=keyboard(
            *(
                RowInfo(
                    factory.create(
                        symbol=FSASymbol.Delete,
                        name=point.name,
                        args=(list(owner.points.values()).index(point),),
                        load=False,
                    )
                )
                for point in owner.points.values()
            ),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

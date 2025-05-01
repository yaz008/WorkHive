from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPublish,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerVacancies,
        FSASymbol.Publish: FSAState.OwnerPublishDone,
    },
)
def owner_point_payload(owner: Owner, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
        ),
        keyboard=keyboard(
            *(
                RowInfo(
                    factory.create(
                        symbol=FSASymbol.Publish,
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

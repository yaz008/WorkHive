from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerIncorrectPromocode,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Ok: FSAState.OwnerSubstription,
    },
)
def owner_settings(owner: Owner, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Ok)),
        ),
    )

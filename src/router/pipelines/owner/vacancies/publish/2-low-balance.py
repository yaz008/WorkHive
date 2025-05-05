from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerLowBalance,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Promocode: FSAState.OwnerPromocode,
        FSASymbol.Ok: FSAState.OwnerVacancies,
    },
)
def owner_point_payload(owner: Owner, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'publications': lambda _: str(owner.balance.publications),
                'tokens': lambda _: str(owner.balance.tokens),
            },
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Promocode)),
            RowInfo(factory.saved(WorkHiveButton.Ok)),
        ),
    )

from model.tables import _Metadata, _Balance, balance_table
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPromocode,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.InputData: FSAState.OwnerPromocode,
        FSASymbol.Back: FSAState.OwnerSubstription,
        FSASymbol.Apply: FSAState.OwnerCorrectPromocode,
        FSASymbol.Error: FSAState.OwnerIncorrectPromocode,
    },
    accepts_types=('text',),
)
def owner_settings(
    owner: Owner, factory: ButtonFactoryClosure, promocode: str
) -> TGMessage:
    if promocode == 'WorkHive10' and promocode not in [
        metadata.value for metadata in owner.metadata.values()
    ]:
        owner.metadata |= {owner.workhive_id: _Metadata(promocode)}
        balance_table.update(
            {
                owner.workhive_id: _Balance(
                    owner.balance.publications + 10, owner.balance.tokens
                )
            }
        )
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'promocode': lambda default: str(
                    promocode if promocode != str() else default
                ),
            },
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(WorkHiveButton.Apply)
                if promocode == 'WorkHive10'
                else factory.saved(WorkHiveButton.ApplyErr)
            ),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

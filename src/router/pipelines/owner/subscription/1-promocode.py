from model.tables import _Metadata, _Balance, balance_table
from model.types import Owner
from project.configs import (
    FSAState,
    FSASymbol,
    FSAPipeline,
    WorkHiveButton,
    PromocodeConfig,
    Promocode,
)
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPromocode,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.InputData: FSAState.OwnerPromocode,
        FSASymbol.Back: FSAState.OwnerSubscription,
        FSASymbol.Apply: FSAState.OwnerCorrectPromocode,
        FSASymbol.Error: FSAState.OwnerIncorrectPromocode,
    },
    accepts_types=('text',),
)
def owner_promocode(
    owner: Owner, factory: ButtonFactoryClosure, promocode_string: str
) -> TGMessage:
    promocode: Promocode | None = PromocodeConfig.Promocodes.get(promocode_string)
    is_promocode_valid: bool = (
        promocode is not None
        and not promocode.is_expired
        and promocode_string
        not in [metadata.value for metadata in owner.metadata.values()]
    )
    if is_promocode_valid:
        assert promocode is not None
        owner.metadata |= {owner.workhive_id: _Metadata(promocode_string)}
        balance_table.update(
            {
                owner.workhive_id: _Balance(
                    owner.balance.publications + promocode.vacancies,
                    owner.balance.tokens + promocode.tokens,
                )
            }
        )
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'promocode': lambda default: str(
                    promocode_string if promocode_string != str() else default
                ),
            },
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(WorkHiveButton.Apply)
                if is_promocode_valid
                else factory.saved(WorkHiveButton.ApplyErr)
            ),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

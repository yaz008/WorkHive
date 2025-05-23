from model.tables import simple_vacancies_table
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.utils import in_metadata


@router.add(
    name=FSAState.OwnerPoints,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Open: FSAState.OwnerPoint,
        FSASymbol.Add: FSAState.OwnerPointAddress,
        FSASymbol.MainMenu: FSAState.OwnerMainMenu,
    },
)
def handler(owner: Owner, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=(
                owner.state
                if in_metadata(owner, 'has-added-point')
                else 'owner-points-fst'
            ),
        ),
        keyboard=keyboard(
            *(
                RowInfo(
                    factory.create(
                        symbol=FSASymbol.Open,
                        name=(
                            f'⏱️ {point.name}'
                            if any(
                                vacancy.point_id == point.__sql_id__
                                for vacancy in simple_vacancies_table[
                                    owner.workhive_id
                                ].values()
                                if not vacancy.is_expired
                            )
                            else point.name
                        ),
                        args=(list(owner.points.values()).index(point), False),
                        load=False,
                    )
                )
                for point in owner.points.values()
            ),
            RowInfo(
                factory.saved(WorkHiveButton.MainMenu),
                factory.saved(WorkHiveButton.Add),
            ),
        ),
    )

from model.tables import simple_vacancies_table
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerVacancyDelete,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerVacancies,
        FSASymbol.Delete: FSAState.OwnerVacancyDelete,
    },
)
def owner_point_payload(
    owner: Owner, factory: ButtonFactoryClosure, index: str
) -> TGMessage:
    if index != str():
        simple_vacancies_table.remove_one(
            owner.workhive_id,
            list(owner.simple_vacancies.values())[int(index)].__sql_id__,
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
                        name=' '.join(
                            (
                                f'{owner.points[vacancy.point_id].name}',
                                f'({vacancy.__sql_id__})',
                            )
                        ),
                        args=(list(owner.simple_vacancies.values()).index(vacancy),),
                        load=False,
                    )
                )
                for vacancy in owner.simple_vacancies.values()
            ),
            RowInfo(factory.saved(WorkHiveButton.Back)),
        ),
    )

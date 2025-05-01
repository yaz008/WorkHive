from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerVacancies,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.MainMenu: FSAState.OwnerMainMenu,
        FSASymbol.Publish: FSAState.OwnerPublish,
        FSASymbol.Error: FSAState.OwnerLowBalance,
        FSASymbol.Delete: FSAState.OwnerVacancyDelete,
    },
)
def register(owner: Owner, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'vacancies': lambda default: (
                    '\n'.join(
                        ' '.join(
                            (
                                f'{index}:',
                                f'{owner.points[vacancy.point_id].name}',
                                f'({vacancy.__sql_id__})',
                            )
                        )
                        for index, vacancy in enumerate(
                            owner.simple_vacancies.values(), start=1
                        )
                    )
                    if len(owner.simple_vacancies) > 0
                    else default
                )
            },
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(
                    WorkHiveButton.Publish
                    if owner.balance.publications > 0
                    else WorkHiveButton.PublishErr
                )
            ),
            RowInfo(factory.saved(WorkHiveButton.Delete)),
            RowInfo(factory.saved(WorkHiveButton.MainMenu)),
        ),
    )

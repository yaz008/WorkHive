from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.utils import in_metadata, add_metadata


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
    if not in_metadata(owner, 'has-published-vacancy'):
        add_metadata(owner, 'has-published-vacancy')
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={
                'vacancies': lambda placeholder: (
                    '\n'.join(
                        ' '.join(
                            (
                                f'{index}:',
                                f'{owner.points[vacancy.point_id].name}',
                                f'({str(vacancy.__sql_id__)[:6]})',
                            )
                        )
                        for index, vacancy in enumerate(
                            owner.simple_vacancies.values(), start=1
                        )
                        if not vacancy.is_expired
                    )
                    if len(owner.simple_vacancies) > 0
                    else f'<i>{placeholder}</i>'
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

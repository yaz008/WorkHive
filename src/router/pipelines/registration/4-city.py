from model.types import TempUser
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.utils import find_closest


@router.add(
    name=FSAState.City,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.TermsOfUseConsent,
        FSASymbol.InputData: FSAState.City,
        FSASymbol.Next: FSAState.WorkerMainMenu,
    },
    accepts_types=('text',),
)
def city(user: TempUser, factory: ButtonFactoryClosure, city: str = str()) -> TGMessage:
    user.city = find_closest(city) if city != str() else str()
    return TGMessage(
        text=render_file(
            language=user.language,
            state=FSAState.City,
            tag_handlers={
                'city': (
                    lambda placeholder: f'<code>{(
                        user.city if user.city != str() else placeholder
                    )}</code>'
                )
            },
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(WorkHiveButton.Back, args=(user.role,)),
                (factory.saved(WorkHiveButton.Next) if user.city != str() else None),
            ),
        ),
    )

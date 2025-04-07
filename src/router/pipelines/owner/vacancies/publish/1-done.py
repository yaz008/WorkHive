from datetime import datetime, timedelta

from model.tables import _VacancySimple, _Point
from model.types import Owner
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerPublishDone,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Next: FSAState.OwnerVacancies,
    },
)
def owner_point_payload(
    owner: Owner, factory: ButtonFactoryClosure, index: str
) -> TGMessage:
    point: _Point = list(owner.points.values())[int(index)]
    vacancy: _VacancySimple = _VacancySimple(
        point_id=point.__sql_id__,
        expiration_time=datetime.now() + timedelta(days=3),
    )
    owner.simple_vacancies |= {vacancy.__sql_id__: vacancy}
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={'name': lambda _: owner.points[vacancy.point_id].name},
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Ok)),
        ),
    )

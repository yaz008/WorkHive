from uuid import uuid4

from model.tables import temp_points, _Point
from model.types import Owner, TempPoint
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router
from router.pipelines.utils import add_metadata


@router.add(
    name=FSAState.OwnerPointDone,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Ok: FSAState.OwnerPoints,
    },
    accepts_types=('text',),
)
def owner_point_done(owner: Owner, factory: ButtonFactoryClosure) -> TGMessage:
    temp_point: TempPoint = TempPoint(owner.telegram_id)
    point: _Point = _Point(
        franchise=temp_point.franchise,
        address=temp_point.address,
        yandex_link=temp_point.yandex_link,
        name=temp_point.name,
        payload=temp_point.payload,
        minimal_charge=temp_point.minimal_charge,
        charge_per_one=temp_point.charge_per_one,
        city=temp_point.city,
        __sql_id__=uuid4(),
    )
    owner.points |= {point.__sql_id__: point}
    add_metadata(owner, 'has-added-point')
    temp_points.remove(temp_point.telegram_id)
    return TGMessage(
        text=render_file(
            language=owner.language,
            state=owner.state,
            tag_handlers={'point-name': lambda _: f'<code>{point.name}</code>'},
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Ok)),
        ),
    )

from model.tables import temp_users
from model.types import User, TempUser, create_user
from project.configs import FSAState, FSAPipeline
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure
from project.libs.tght import render_file
from router.instance import router


@router.add(name=FSAState.OwnerMainMenu, pipeline=FSAPipeline.Owner)
def register(user: User | TempUser, _: ButtonFactoryClosure) -> TGMessage:
    if isinstance(user, TempUser):
        user = create_user(user)
        temp_users.remove(user.telegram_id)
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
    )

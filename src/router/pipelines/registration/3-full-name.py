from itertools import chain

from model.types import TempUser
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


def normalize_name(name: str) -> str:
    return ' '.join(
        filter(
            lambda w: w != str(),
            map(lambda w: w.capitalize(), name.split(sep=' ', maxsplit=5)),
        )
    )


def is_valid_name(normalized_name: str) -> bool:
    if normalized_name == str():
        return False
    words: list[str] = normalized_name.split(sep=' ', maxsplit=5)
    if len(words) not in range(2, 7):
        return False
    return any(
        all(letter in symbolset for letter in chain(*map(lambda w: w.lower(), words)))
        for symbolset in (
            'abcdefghijklmnopqrstuvwxyz',
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
        )
    )


@router.add(
    name=FSAState.FullName,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.Back: FSAState.ChooseRole,
        FSASymbol.Next: FSAState.BirthDate,
        FSASymbol.InputData: FSAState.FullName,
        FSASymbol.Error: FSAState.FullNameErr,
    },
    accepts_types=('text',),
)
def full_name(user: TempUser, factory: ButtonFactoryClosure, name: str) -> TGMessage:
    normalized_name: str = normalize_name(name)
    if normalized_name != str():
        user.full_name = normalized_name
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
            tag_handlers={
                'full-name': lambda placeholder: (
                    f'<code>{user.full_name}</code>'
                    if user.full_name != str()
                    else f'<code>{placeholder}</code>'
                )
            },
        ),
        keyboard=keyboard(
            RowInfo(
                factory.saved(WorkHiveButton.Back, args=(user.role,)),
                (
                    (
                        factory.saved(WorkHiveButton.Next)
                        if is_valid_name(user.full_name)
                        else factory.saved(WorkHiveButton.NextErr)
                    )
                    if user.full_name != str()
                    else None
                ),
            ),
        ),
    )

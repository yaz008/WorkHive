from model.types import User
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton, Language
from project.libs.fsa import serializer
from project.libs.tgdraw import (
    TGMessage,
    ButtonFactoryClosure,
    ButtonInfo,
    RowInfo,
    load_button,
    choice,
)
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.OwnerLanguage,
    pipeline=FSAPipeline.Owner,
    transitions={
        FSASymbol.Back: FSAState.OwnerSettings,
        FSASymbol.InputData: FSAState.OwnerLanguage,
    },
)
def owner_language(
    user: User, factory: ButtonFactoryClosure, language: str
) -> TGMessage:
    user.language = language
    return TGMessage(
        text=render_file(
            language=user.language,
            state=user.state,
        ),
        keyboard=choice(
            tuple(
                factory.create(
                    symbol=FSASymbol.InputData, name=name, args=(code,), load=False
                )
                for name, code in zip(
                    Language.attrtuple('native_name'), Language.attrtuple('code')
                )
            ),
            Language.attrtuple('code').index(user.language),
            RowInfo(
                ButtonInfo(
                    text=load_button(name=WorkHiveButton.Next, language=user.language),
                    data=serializer.serialize(
                        state=FSAState.ChooseLanguage,
                        symbol=FSASymbol.Next,
                    ),
                ),
            ),
        ),
    )

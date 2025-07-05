from model.types import TempUser
from project.configs import Language, FSAState, FSASymbol, FSAPipeline, WorkHiveButton
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
    name=FSAState.ChooseLanguage,
    pipeline=FSAPipeline.Registration,
    transitions={
        FSASymbol.InputData: FSAState.ChooseLanguage,
        FSASymbol.Next: FSAState.ChooseRole,
    },
)
def choose_language(
    user: TempUser, factory: ButtonFactoryClosure, language: str
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
                        args=(user.role,),
                    ),
                ),
            ),
        ),
    )

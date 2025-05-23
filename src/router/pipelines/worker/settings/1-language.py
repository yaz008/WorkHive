from model.types import Worker
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
    name=FSAState.WorkerLanguage,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.Back: FSAState.WorkerSettings,
        FSASymbol.InputData: FSAState.WorkerLanguage,
    },
)
def worker_choose_language(
    worker: Worker, factory: ButtonFactoryClosure, language: str
) -> TGMessage:
    if language != str():
        worker.language = language
    return TGMessage(
        text=render_file(
            language=worker.language,
            state=worker.state,
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
            Language.attrtuple('code').index(worker.language),
            RowInfo(
                ButtonInfo(
                    text=load_button(
                        name=WorkHiveButton.Back, language=worker.language
                    ),
                    data=serializer.serialize(
                        state=FSAState.WorkerLanguage,
                        symbol=FSASymbol.Back,
                    ),
                ),
            ),
        ),
    )

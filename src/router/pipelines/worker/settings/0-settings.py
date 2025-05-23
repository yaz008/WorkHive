from model.types import Worker
from project.configs import FSAState, FSASymbol, FSAPipeline, WorkHiveButton
from project.libs.tgdraw import TGMessage, ButtonFactoryClosure, RowInfo, keyboard
from project.libs.tght import render_file
from router.instance import router


@router.add(
    name=FSAState.WorkerSettings,
    pipeline=FSAPipeline.Worker,
    transitions={
        FSASymbol.MainMenu: FSAState.WorkerMainMenu,
        FSASymbol.Language: FSAState.WorkerLanguage,
        FSASymbol.AboutProject: FSAState.WorkerAboutProject,
    },
)
def owner_settings(worker: Worker, factory: ButtonFactoryClosure) -> TGMessage:
    return TGMessage(
        text=render_file(
            language=worker.language,
            state=worker.state,
        ),
        keyboard=keyboard(
            RowInfo(factory.saved(WorkHiveButton.Language)),
            RowInfo(factory.saved(WorkHiveButton.AboutProject)),
            RowInfo(factory.saved(WorkHiveButton.MainMenu)),
        ),
    )

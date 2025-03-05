from project.core.config import config


@config(filename='fsa-states')
class FSAState:
    Initial: str = 'initial'
    ChooseLanguage: str = 'choose-language'
    MainMenu: str = 'main-menu'


@config(filename='fsa-symbols')
class FSASymbol:
    Start: str = 'start'
    Next: str = 'next'
    Back: str = 'back'
    InputData: str = 'input-data'


@config(filename='fsa')
class FSAConfig:
    MainDelimiter: str = '$'
    ArgDelimiter: str = ':'
    InitialTransitionState: str = FSAState.ChooseLanguage
    StartTransitionState: str = FSAState.MainMenu

from project.core.config import config


@config(filename='fsa-states')
class FSAState:
    Initial: str = 'initial'
    ChooseLanguage: str = 'choose-language'
    ChooseRole: str = 'choose-role'
    Register: str = 'register'
    FullName: str = 'full-name'
    FullNameCheck: str = 'full-name-check'
    BirthDate: str = 'birth-date'
    PrivacyPolicyConcent: str = 'privacy-policy-concent'
    AdReceiveingConcent: str = 'ad-receiveing-concent'
    OfferAgreementConcent: str = 'offer-agreement-concent'
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

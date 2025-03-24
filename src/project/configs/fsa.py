from project.core.config import config


@config(filename='fsa-states')
class FSAState:
    Initial: str = 'initial'

    # Registration
    ChooseLanguage: str = 'choose-language'
    ChooseRole: str = 'choose-role'
    Register: str = 'register'
    FullName: str = 'full-name'
    FullNameErr: str = 'full-name-err'
    BirthDate: str = 'birth-date'
    BirthDateErr: str = 'birth-date-err'
    PrivacyPolicyConsent: str = 'privacy-policy-consent'
    AdvertisingConsent: str = 'advertising-consent'
    OfferConsent: str = 'offer-consent'

    # Owner
    OwnerMainMenu: str = 'owner-main-menu'

    # Worker
    WorkerMainMenu: str = 'worker-main-menu'


@config(filename='fsa-symbols')
class FSASymbol:
    Start: str = 'start'
    Next: str = 'next'
    Back: str = 'back'
    InputData: str = 'input-data'
    Error: str = 'error'


@config(filename='fsa')
class FSAConfig:
    MainDelimiter: str = '$'
    ArgDelimiter: str = ':'
    InitialTransitionState: str = FSAState.ChooseLanguage


@config(filename='fsa-pipeline')
class FSAPipeline:
    Registration: str = 'registration'
    Owner: str = 'owner'
    Worker: str = 'worker'

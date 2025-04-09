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
    OwnerSettings: str = 'owner-settings'
    OwnerPoints: str = 'owner-points'
    OwnerVacancies: str = 'owner-vacancies'
    OwnerNotifications: str = 'owner-notifications'
    OwnerNotification: str = 'owner-notification'
    OwnerSubstription: str = 'owner-subscription'

    OwnerLanguage: str = 'owner-language'

    OwnerPointAddress: str = 'owner-point-address'
    OwnerPointPayload: str = 'owner-point-payload'
    OwnerPointCharge: str = 'owner-point-charge'
    OwnerPointChargePerOne: str = 'owner-point-charge-per-one'
    OwnerPointName: str = 'owner-point-name'
    OwnerPointDone: str = 'owner-point-done'
    OwnerPointDelete: str = 'owner-point-delete'

    OwnerPublish: str = 'owner-publish'
    OwnerPublishDone: str = 'owner-publish-done'
    OwnerVacancyDelete: str = 'owner-vacancy-delete'

    # Worker
    WorkerMainMenu: str = 'worker-main-menu'

    WorkerSettings: str = 'worker-settings'
    WorkerLanguage: str = 'worker-language'

    WorkerResponds: str = 'worker-responds'

    Search: str = 'search'
    WorkerSearch: str = 'worker-search'
    WorkerSearchResults: str = 'worker-search-results'
    WorkerSearchNoResults: str = 'worker-search-no-results'
    Respond: str = 'respond'


@config(filename='fsa-symbols')
class FSASymbol:
    Start: str = 'start'
    Next: str = 'next'
    Back: str = 'back'
    InputData: str = 'input-data'
    Error: str = 'error'

    # Menus:
    Settings: str = 'settings'
    Publish: str = 'publish'
    Points: str = 'points'
    Vacancies: str = 'vacancies'
    Notifications: str = 'notifications'
    Subscription: str = 'subscription'
    Language: str = 'language'
    Responds: str = 'responds'

    # Actions:
    Add: str = 'add'
    Delete: str = 'delete'
    Search: str = 'search'
    Respond: str = 'respond'
    View: str = 'view'
    Open: str = 'open'
    Ok: str = 'ok'


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

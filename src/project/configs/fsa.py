from project.core.config import config


@config(filename='fsa-states')
class FSAState:
    Initial: str = 'initial'

    # Registration
    ChooseLanguage: str = 'registration-choose-language'
    Register: str = 'registration-register'
    ChooseRole: str = 'registration-choose-role'
    HowItWorks: str = 'registration-how-it-works'
    FullName: str = 'registration-full-name'
    FullNameErr: str = 'registration-full-name-err'
    BirthDate: str = 'registration-birth-date'
    BirthDateErr: str = 'registration-birth-date-err'
    # PrivacyPolicyConsent: str = 'registration-privacy-policy-consent'
    # AdvertisingConsent: str = 'registration-advertising-consent'
    # OfferConsent: str = 'registration-offer-consent'
    TermsOfUseConsent: str = 'registration-terms-of-use-consent'
    City: str = 'registration-city'

    # Owner
    OwnerNoADConsent: str = 'owner-no-ad-consent'

    OwnerMainMenu: str = 'owner-main-menu'
    OwnerSettings: str = 'owner-settings'
    OwnerRevokeConsentConfirm: str = 'owner-revoke-concent-confirm'
    OwnerAboutProject: str = 'owner-about-project'
    OwnerVacancies: str = 'owner-vacancies'
    OwnerNotification: str = 'owner-notification'

    OwnerLanguage: str = 'owner-language'

    OwnerPointAddress: str = 'owner-point-address'
    OwnerPointCity: str = 'owner-point-city'
    OwnerPointPayload: str = 'owner-point-payload'
    OwnerPointCharge: str = 'owner-point-charge'
    OwnerPointChargePerOne: str = 'owner-point-charge-per-one'
    OwnerPointName: str = 'owner-point-name'
    OwnerPointDone: str = 'owner-point-done'

    OwnerPointDelete: str = 'owner-point-delete'

    OwnerPointAddressEdit: str = 'owner-point-address-edit'
    OwnerPointPayloadEdit: str = 'owner-point-payload-edit'
    OwnerPointChargeEdit: str = 'owner-point-charge-edit'
    OwnerPointChargePerOneEdit: str = 'owner-point-charge-per-one-edit'
    OwnerPointNameEdit: str = 'owner-point-name-edit'
    OwnerPointDoneEdit: str = 'owner-point-done-edit'

    OwnerPoints: str = 'owner-points'
    OwnerPoint: str = 'owner-point'
    OwnerPointDeleted: str = 'owner-point-deleted'
    OwnerPointDeletionConfirm: str = 'owner-point-deletion-confirm'

    OwnerPublish: str = 'owner-publish'
    OwnerPublishDone: str = 'owner-publish-done'
    OwnerLowBalance: str = 'owner-no-balance'
    OwnerVacancyDelete: str = 'owner-vacancy-delete'

    OwnerNotifications: str = 'owner-notifications'
    OwnerNoNotifications: str = 'owner-no-notifications'
    OwnerNotificationDeclined: str = 'owner-notification-declined'
    OwnerNotificationAccepted: str = 'owner-notification-accepted'

    OwnerAcceptedResponses: str = 'owner-accepted-responses'
    OwnerNoAcceptedResponses: str = 'owner-no-accepted-responses'

    OwnerSubscription: str = 'owner-subscription'
    OwnerPromocode: str = 'owner-promocode'
    OwnerCorrectPromocode: str = 'owner-correct-promocode'
    OwnerIncorrectPromocode: str = 'owner-incorrect-promocode'

    # Worker
    WorkerNoADConsent: str = 'worker-no-ad-consent'

    WorkerMainMenu: str = 'worker-main-menu'

    WorkerSettings: str = 'worker-settings'
    WorkerAboutProject: str = 'worker-about-project'
    WorkerRevokeConsentConfirm: str = 'worker-revoke-concent-confirm'
    WorkerLanguage: str = 'worker-language'

    WorkerResponds: str = 'worker-responds'
    WorkerNoResponds: str = 'worker-no-responds'

    WorkerAcceptedResponds: str = 'worker-accepted-responds'
    WorkerNoAcceptedResponds: str = 'worker-no-accepted-responds'

    Search: str = 'search'
    WorkerSearch: str = 'worker-search'
    WorkerSearchResults: str = 'worker-search-results'
    WorkerSearchNoResults: str = 'worker-search-no-results'
    Respond: str = 'respond'

    # Driver
    DriverOnOwnerNewNotification: str = 'driver-on-owner-new-notification'
    DriverOnWorkerNewNotification: str = 'driver-on-worker-new-notification'


@config(filename='fsa-symbols')
class FSASymbol:
    Start: str = 'start'
    Next: str = 'next'
    Back: str = 'back'
    InputData: str = 'input-data'
    Error: str = 'error'
    Yes: str = 'yes'
    No: str = 'no'

    # Menus:
    MainMenu: str = 'main-menu'
    Settings: str = 'settings'
    Publish: str = 'publish'
    Points: str = 'points'
    Vacancies: str = 'vacancies'
    Notifications: str = 'notifications'
    Subscription: str = 'subscription'
    Language: str = 'language'
    Responds: str = 'responds'
    AcceptedResponses: str = 'accepted-responses'
    Promocode: str = 'promocode'
    AboutProject: str = 'about-project'
    HowItWorks: str = 'how-it-works'

    # Actions:
    Add: str = 'add'
    Delete: str = 'delete'
    Search: str = 'search'
    Respond: str = 'respond'
    View: str = 'view'
    Open: str = 'open'
    Ok: str = 'ok'
    Accept: str = 'accept'
    Decline: str = 'decline'
    Apply: str = 'apply'
    Skip: str = 'skip'
    Edit: str = 'edit'
    Revoke: str = 'revoke'
    Confirm: str = 'confirm'
    Contact: str = 'contact'
    Subscribe: str = 'subscribe'
    FollowLink: str = 'follow-link'


@config(filename='fsa')
class FSAConfig:
    MainDelimiter: str = '$'
    ArgDelimiter: str = '#'
    InitialTransitionState: str = FSAState.ChooseLanguage


@config(filename='fsa-pipeline')
class FSAPipeline:
    Registration: str = 'registration'
    Owner: str = 'owner'
    OwnerNoADConsent: str = 'owner-no-ad-consent'
    Worker: str = 'worker'
    WorkerNoADConsent: str = 'worker-no-ad-consent'

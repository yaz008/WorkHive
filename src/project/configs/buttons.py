from project.core.config import config


@config(filename='buttons')
class ButtonConfig:
    ButtonsFolder: str = 'assets\\buttons'
    Checked: str = '✅'
    CheckDelimiter: str = ' '


@config(filename='button-names')
class WorkHiveButton:
    # Navigation:
    Next: str = 'next'
    NextErr: str = 'next-err'
    Back: str = 'back'
    Ok: str = 'ok'

    # Actions:
    Register: str = 'register'
    Consent: str = 'consent'
    DeleteAccount: str = 'delete-account'
    Post: str = 'post'
    Add: str = 'add'
    Delete: str = 'delete'
    Edit: str = 'edit'
    Hide: str = 'hide'
    ShowContact: str = 'show-contact'
    Accept: str = 'accept'
    Decline: str = 'decline'
    Subscribe: str = 'subscribe'
    Publish: str = 'publish'
    PublishErr: str = 'publish-err'
    Search: str = 'search'
    Respond: str = 'respond'
    Apply: str = 'apply'
    ApplyErr: str = 'apply-err'

    # Menus:
    MainMenu: str = 'main-menu'
    Settings: str = 'settings'
    NotificationSettings: str = 'notification-settings'
    Notifications: str = 'notifications'
    NotificationsNew: str = 'notifications-new'
    MyPoints: str = 'my-points'
    MyVacancies: str = 'my-vacancies'
    MyResponds: str = 'my-responds'
    AcceptedResponses: str = 'accepted-responses'
    AcceptedResponsesNew: str = 'accepted-responses-new'
    Promocode: str = 'promocode'

    # Other:
    Worker: str = 'worker'
    Owner: str = 'owner'
    Language: str = 'language'
    Subsrciption: str = 'subscription'

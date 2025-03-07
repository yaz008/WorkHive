from project.core.config import config


@config(filename='buttons')
class ButtonConfig:
    ButtonsFolder: str = 'assets\\buttons'
    Checked: str = '✅'
    NotChecked: str = '☑️'
    CheckDelimiter: str = ' '


@config(filename='button-names')
class WorkHiveButton:
    Next: str = 'next'
    Back: str = 'back'
    Register: str = 'register'
    Worker: str = 'worker'
    Owner: str = 'owner'
    Concent: str = 'concent'

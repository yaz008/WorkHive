from project.core.config import config


@config(filename='fsa-symbols')
class FSASymbol:
    Start: str = 'start'
    Next: str = 'next'
    Back: str = 'back'
    InputData: str = 'input-data'

from project.core.config import config


@config(filename='buttons')
class BlacklistConfig:
    BasePath: str = 'blacklist'
    Filename: str = 'banned'

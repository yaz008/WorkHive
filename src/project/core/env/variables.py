from project.core.env.var import EnvVar


class Env:
    TELEGRAM_BOT_TOKEN = EnvVar(
        name='TELEGRAM_BOT_TOKEN', pattern=r'^\d{1,10}:[A-Za-z0-9_-]{35}$'
    )

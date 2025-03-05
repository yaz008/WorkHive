from project.configs import TGDriverConfig
from project.core.env import Env
from project.libs.tgdraw import TGDriver


driver: TGDriver = TGDriver(
    token=Env.TELEGRAM_BOT_TOKEN,
    parse_mode=TGDriverConfig.DefaultParseMode,
    skip_pending=TGDriverConfig.SkipPending,
    threads=TGDriverConfig.Threads,
)

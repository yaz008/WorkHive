from time import time
from typing import Callable

from model.logger import Logger


response_time_logger: Logger = Logger(logfile='response-time')


def measure_time[**Args, Ret](func: Callable[Args, Ret]) -> Callable[Args, Ret]:
    def wrapper(*args: Args.args, **kwargs: Args.kwargs) -> Ret:
        start: float = time()
        ret: Ret = func(*args, **kwargs)
        execution_time: float = time() - start
        response_time_logger.write(
            message=f'{func.__name__}() ran in {execution_time} sec',
            execution_time=str(execution_time),
            function=func.__name__,
        )
        return ret

    return wrapper

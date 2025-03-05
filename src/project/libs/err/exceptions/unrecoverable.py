from project.core.exceptions import BaseWorkHiveException, IncorrectExceptionUsageError


class MutuallyExclusiveArgumentsError(BaseWorkHiveException):
    def __init__(self, *argnames: str) -> None:
        if len(argnames) < 2:
            raise IncorrectExceptionUsageError(
                exception=self,
                message=f'Expected at least 2 argnames, got {len(argnames)}',
            )
        args: str = (
            f'{', '.join(
                map(lambda arg: f'\"{arg}\"', argnames[:-1])
            )} and \"{argnames[-1]}\"'
        )
        super().__init__(f'Arguments {args} are mutually exclusive')

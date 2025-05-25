from dataclasses import dataclass
from datetime import datetime
from json import dumps


@dataclass(slots=True)
class Logger:
    logfile: str

    def write(self, message: str, **attrs: str) -> None:
        with open(f'logs/{self.logfile}.jsonl', mode='a', encoding='UTF-8') as logfile:
            logfile.write(
                dumps(
                    {
                        'datetime': datetime.now().strftime('%d.%m.%Y-%H:%M:%S:%f'),
                        'message': message,
                    }
                    | {name: value for name, value in attrs.items()}
                )
                + '\n'
            )

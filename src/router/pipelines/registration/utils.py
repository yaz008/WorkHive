from datetime import datetime, timedelta


def render_birth_date(placeholder: str, birth_date: str) -> str:
    result: str = placeholder
    for digit in birth_date:
        result = result.replace('_', digit, count=1)
    return result


def is_birth_date_valid(birth_date: datetime | None) -> bool:
    if birth_date is None:
        return False
    age: timedelta = datetime.now() - birth_date
    return timedelta(14 * 365 + 3) < age < timedelta(120 * 365 + 30)

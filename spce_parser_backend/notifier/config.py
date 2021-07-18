from datetime import time, timedelta


TIMED_NOTIFICATIONS = [time(hour=6, minute=30),
                       time(hour=10, minute=30),
                       time(hour=16, minute=0),
                       time(hour=22, minute=15)]


class NotifInitError(Exception):
    ...


def get_str_percent(now, last) -> str:
    percents = 100 - (now * 100 / last)

    if now < last:
        prefix = '+'
    else:
        prefix = ''

    result = prefix + str(round(percents, 1)) + '%'

    return result

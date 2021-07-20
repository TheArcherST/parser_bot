from .config import TIMED_NOTIFICATIONS, NotifInitError, get_str_percent
from datetime import date, datetime, time, timedelta, timezone
from mailing import mailing
from ..types import UpdateFrame
from ..db_helper import SPCEHistoryDB, SPCEShortsHistoryDB


spce_history_db = SPCEHistoryDB()
spce_shorts_history_db = SPCEShortsHistoryDB()


class TimedNotifier:
    def __init__(self):
        df = spce_history_db.get_df(7)
        if len(df) < 7:
            raise NotifInitError

        yesterday = df.iloc[0]

        week_ago_df = df.iloc[:7]
        week_ago = week_ago_df.mean(numeric_only=True)


        self.cost_last_day_position = (yesterday.opening_price + yesterday.closing_price) / 2
        self.volume_last_day_position = yesterday.volume
        self.cost_last_week_position = (week_ago.opening_price + week_ago.closing_price) / 2
        self.volume_last_week_position = week_ago.volume


        df = spce_shorts_history_db.get_df(7)
        if len(df) < 7:
            raise NotifInitError

        yesterday = df.iloc[0]

        week_ago_df = df.iloc[:7]
        week_ago = week_ago_df.mean(numeric_only=True)

        self.shorts_last_day_position = yesterday.total_shares
        self.shorts_last_week_position = week_ago.total_shares

        self.sent_notifications = list()

    def accept_updates(self, last_updates: UpdateFrame):
        today = datetime.utcnow() + timedelta(hours=3)
        notif_times = [datetime(year=today.year, month=today.month,
                       day=today.day, hour=i.hour, minute=i.minute)
                       for i in TIMED_NOTIFICATIONS]

        for notif, notif_time in zip(TIMED_NOTIFICATIONS, notif_times):
            now = datetime.utcnow() + timedelta(hours=3)

            if now > notif_time and now - timedelta(minutes=5) < notif_time and notif not in self.sent_notifications:
                self.sent_notifications.append(notif)
                self.send_report(last_updates)
                break

    def send_report(self, last_updates: UpdateFrame):
        cost = last_updates.data_price.cost
        volume = last_updates.data_price.volume
        short = last_updates.data_shorts.current_short_volume

        cost_day_percent = get_str_percent(self.cost_last_day_position, cost)
        cost_week_percent = get_str_percent(self.cost_last_week_position, cost)

        volume_day_percent = get_str_percent(self.volume_last_day_position, volume)
        volume_week_percent = get_str_percent(self.volume_last_week_position, volume)

        shorts_day_percent = get_str_percent(self.shorts_last_day_position, short)
        shorts_week_percent = get_str_percent(self.shorts_last_week_position, short)

        mailing(f"""

*Плановое уведомление*

- Цена равна ${cost}
За день {cost_day_percent}
За неделю {cost_week_percent}

- Объём равен {volume / 10 ** 6} млн акций
За день {volume_day_percent}
За неделю {volume_week_percent}

- Объём шорта равен {short / 10 ** 6} млн акций
За день {shorts_day_percent}
За неделю {shorts_week_percent}

""", 'spce')

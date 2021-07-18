from ..config import COST_NOTIFY_STEP, VOLUME_NOTIFY_STEP
from typing import Union
from mailing import mailing
from ..types import UpdateFrame
from ..db_helper import SPCEHistoryDB
from datetime import date, datetime, timedelta
from .config import NotifInitError, get_str_percent


spce_history_db = SPCEHistoryDB()


class NotifyEntity:
    def __init__(self, start_position: Union[int, float], percent_step: Union[int, float]):
        self.start_position = start_position
        self.percent_step = percent_step

        self.notification_count = 0

    def accept_value(self, new_value: Union[int, float]):

        excepted_change_percent = self.percent_step * (self.notification_count + 1)
        excepted_change = self.start_position * excepted_change_percent / 100
        excepted_value_low = self.start_position - excepted_change
        excepted_value_high = self.start_position + excepted_change

        if new_value >= excepted_value_high or new_value <= excepted_value_low:
            self.send_notification(new_value)
            self.notification_count += 1

    def send_notification(self, new_value: Union[int, float]):
        text = self.get_notification_text(new_value)
        mailing(text)

    def get_notification_text(self, new_value: Union[int, float]) -> str:
        pass


class NotifyEntityCost(NotifyEntity):
    def get_notification_text(self, new_value: Union[int, float]):
        percent = get_str_percent(self.start_position, new_value)

        return f"""
*Срочное уведомление - цена*

Цена равна ${new_value} ({percent})
"""


class NotifyEntityVolume(NotifyEntity):
    def get_notification_text(self, new_value: Union[int, float]):
        percent = get_str_percent(self.start_position, new_value)

        return (f"""
*Срочное уведомление - объём*

Объём равен ${round(new_value / 10 ** 6, 2)} млн ({percent})
""")


class EmergencyNotifier:
    def __init__(self):
        df = spce_history_db.get_df(7)
        if len(df) < 7:
            raise NotifInitError

        yesterday = df.iloc[1]

        cost_last_day_position = (yesterday.opening_price + yesterday.closing_price) / 2
        volume_last_day_position = yesterday.volume

        self.cost = NotifyEntityCost(
            cost_last_day_position, COST_NOTIFY_STEP
        )
        self.volume = NotifyEntityVolume(
            volume_last_day_position, VOLUME_NOTIFY_STEP
        )

    def accept_updates(self, updates: UpdateFrame):
        self.cost.accept_value(updates.data_price.cost)
        self.volume.accept_value(updates.data_price.volume)

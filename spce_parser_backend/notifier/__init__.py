from .emergency_notifier import EmergencyNotifier
from .timed_notifier import TimedNotifier
from ..types import UpdateFrame
from .config import NotifInitError


class Notifier:
    def __init__(self):
        """ Initialize it only past your server get first updates """
        
        self.emergency = EmergencyNotifier()
        self.timed = TimedNotifier()

    def accept_updates(self, updates: UpdateFrame):
        """ This function need connect to updates thread """

        self.emergency.accept_updates(updates)
        self.timed.accept_updates(updates)

    def reset(self):
        self.emergency = EmergencyNotifier()
        self.timed = TimedNotifier()

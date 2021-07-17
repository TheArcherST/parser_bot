from threading import Thread
from .types import UpdateFrame, get_new_options_chains
from .db_helper import SPCEDB, SPCEOptionsChainDB
from datetime import datetime, timedelta
from .config import UPDATES_TIMEOUT_SEC, HISTORY_WRITE_TIMEOUT_H
from .parse_helper import get_price_data, get_shorts_data, get_options_chain
import requests


spce_options_db = SPCEOptionsChainDB()
spce_db = SPCEDB()


def is_connection():
    try:
        requests.get('https://www.google.ru/')
    except:
        return False
    return True


class Server:
    def __init__(self, update_timeout_sec=None, history_update_timeout_h=None):
        if update_timeout_sec is None:
            update_timeout_sec = UPDATES_TIMEOUT_SEC
        if history_update_timeout_h is None:
            history_update_timeout_h = HISTORY_WRITE_TIMEOUT_H

        self.update_delta = timedelta(seconds=update_timeout_sec)
        self.history_update_delta = timedelta(hours=history_update_timeout_h)
        self.is_run = False
        self.last_history_upd = None

    def start(self):
        if not is_connection():
            return False

        self.is_run = True
        thread = Thread(target=self._flow)
        thread.start()

        return True

    def stop(self):
        self.is_run = False

    def _flow(self):
        while True:
            if self.last_history_upd is None:
                self.accept_updates(True)
                self.last_history_upd = datetime.now()
            elif self.last_history_upd + self.history_update_delta <= datetime.now():
                self.accept_updates(True)
                self.last_history_upd = datetime.now()
            else:
                self.accept_updates(False)

            if not self.is_run:
                break

    def accept_updates(self, to_write_history=False):
        updates = self._get_updates()

        if to_write_history:
            spce_db.write_updates(updates)

        spce_options_db.write_updates(updates.new_options_chains)


    def _get_updates(self):
        price_data = get_price_data()
        shorts_data = get_shorts_data()
        options_chain = get_options_chain()

        old_options_chain = spce_options_db.get_df(50)
        if len(old_options_chain) < 50:
            old_options_chain = None

        new = options_chain.df
        new_chains = get_new_options_chains(old_options_chain, new)

        result = UpdateFrame(price_data, shorts_data, new_chains)

        return result

    def __exit__(self):
        self.stop()

    def __del__(self):
        self.stop()

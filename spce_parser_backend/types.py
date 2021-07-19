from typing import List
import pandas as pd
import numpy as np
from datetime import datetime, date
from .config import CHAIN_EQ_CHECK
from typing import Union
import pytest


class DataPrice:
    def __init__(self, cost: float, volume: int, average_volume: int):
        self.cost = cost
        self.volume = volume
        self.average_volume = average_volume

    def __repr__(self):
        return f'DataPrice(cost={self.cost}, volume={self.volume}, average_volume={self.average_volume})'

    def __str__(self):
        return repr(self)


class DataShorts:
    def __init__(self, current_short_volume, previous_short_volume):
        self.current_short_volume = current_short_volume
        self.previous_short_volume = previous_short_volume

    def __repr__(self):
        return f'DataShorts(current_short_volume={self.current_short_volume}, previous_short_volume={self.previous_short_volume})'

    def __str__(self):
        return repr(self)


class DataOptionsChain:  # raw data
    def __init__(self, expires: List[date], strike_price: List[float], put_or_call: List[str], volume: List[float]):
        self.expires = expires
        self.strike_price = strike_price
        self.put_or_call = put_or_call
        self.volume = volume

    @property
    def df(self):
        return pd.DataFrame(
            {'expires': self.expires,
             'strike_price': self.strike_price,
             'put_or_call': self.put_or_call,
             'volume': self.volume}
        )

    def __repr__(self):
        return f"DataOptionsChain(expires={self.expires}, strike_price={self.strike_price}, put_or_call={self.put_or_call}, volume={self.volume})"

    def __str__(self):
        return str(self.df)


class DataHistory:  # raw data
    def __init__(self, date: List[date], opening_price: List[float], closing_price: List[float], volume: List[float]):
        self.date = date
        self.opening_price = opening_price
        self.closing_price = closing_price
        self.volume = volume

    @property
    def df(self):
        return pd.DataFrame(
            {'date': self.date,
             'opening_price': self.opening_price,
             'closing_price': self.closing_price,
             'volume': self.volume}
        )

    def __repr__(self):
        return f"DataHistory(date={self.date}, opening_price={self.opening_price}, closing_price={self.closing_price}, volume={self.volume})"

    def __str__(self):
        return str(self.df)


class DataShortsHistory:
    def __init__(self, date: List[date], total_shares: List[int], volume: List[float]):
        self.date = date
        self.total_shares = total_shares
        self.volume = volume

    @property
    def df(self):
        return pd.DataFrame(
            {'date': self.date,
             'total_shares': self.total_shares,
             'volume': self.volume}
        )

    def __repr__(self):
        return f"DataShortsHistory(date={self.date}, total_shares={self.total_shares}, volume={self.volume})"

    def __str__(self):
        return str(self.df)


able_convert_to_df = Union[DataOptionsChain, DataHistory, DataShortsHistory]


def get_table_changes(old: Union[able_convert_to_df, pd.DataFrame, None],
                      new: Union[able_convert_to_df, pd.DataFrame], chain_eq_check=None) -> pd.DataFrame:

    if isinstance(old, (DataOptionsChain, DataHistory)):
        old = old.df
    if isinstance(new, (DataOptionsChain, DataHistory)):
        new = new.df

    if old is None:
        return new

    if chain_eq_check is None:
        chain_eq_check = CHAIN_EQ_CHECK


    offset = 0  # what offset have new?

    for row_num in range(len(new)):
        for local_offset in range(chain_eq_check):
            try:
                next_item = list(new.iterrows())[row_num + local_offset][1]
            except IndexError:
                return new

            if not np.all([old.iloc[local_offset] == next_item]):
                offset += 1
                break

        else:  # all equals passed!
            break

    else:  # total: no eq...
        return new

    update = new.iloc[:offset]

    return update


class UpdateFrame:
    def __init__(self, data_price: DataPrice, data_shorts: DataShorts, new_options_chains: pd.DataFrame,
                 new_history: pd.DataFrame, new_shorts_history: pd.DataFrame):
        self.data_price = data_price
        self.data_shorts = data_shorts
        self.new_options_chains = new_options_chains
        self.new_history = new_history
        self.new_shorts_history = new_shorts_history

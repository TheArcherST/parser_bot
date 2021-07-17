from typing import List
import pandas as pd
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


def get_new_options_chains(old: Union[DataOptionsChain, pd.DataFrame, None], new: Union[DataOptionsChain, pd.DataFrame], chain_eq_check=None) -> pd.DataFrame:
    if isinstance(old, DataOptionsChain):
        old = old.df
    if isinstance(new, DataOptionsChain):
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

            if not all([old.expires[local_offset] == next_item[0],
                        old.strike_price[local_offset] == next_item[1],
                        old.put_or_call[local_offset] == next_item[2],
                        old.volume[local_offset] == next_item[3]]):
                offset += 1
                break
        else:  # all equals passed!
            break

    else:  # no eq...
        return new


    update = new.iloc[:offset]

    return update


class UpdateFrame:
    def __init__(self, data_price: DataPrice, data_shorts: DataShorts, new_options_chains: pd.DataFrame):
        self.data_price = data_price
        self.data_shorts = data_shorts
        self.new_options_chains = new_options_chains

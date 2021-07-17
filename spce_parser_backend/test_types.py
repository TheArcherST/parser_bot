import pytest
import pandas as pd
from .types import get_new_options_chains
from .config import CHAIN_EQ_CHECK
from datetime import datetime
import numpy as np


def test_get_new_options_chains():
    d1 = pd.DataFrame(
        {
        'expires': [
            datetime(year=2000, month=1, day=1),
            datetime(year=2000, month=1, day=1),
            datetime(year=2000, month=1, day=1),
            datetime(year=2000, month=1, day=1),
        ],
        'strike_price': [
            1,
            1,
            1,
            1
        ],
        'put_or_call': [
            'call',
            'call',
            'call',
            'call'
        ],
        'volume': [
            1,
            2,
            3,
            4
        ]
        }
    )

    d2 = pd.DataFrame(
        {
        'expires': [
            datetime(year=2000, month=6, day=1),
            datetime(year=2000, month=1, day=1),
            datetime(year=2000, month=1, day=1),
            datetime(year=2000, month=1, day=1)
        ],
        'strike_price': [
            1,
            1,
            1,
            1
        ],
        'put_or_call': [
            'call',
            'call',
            'call',
            'call'
        ],
        'volume': [
            6,
            1,
            2,
            3
        ]
        }
    )
    result = get_new_options_chains(d1, d2, 3)

    expected = pd.DataFrame(
        {
        'expires': [
            datetime(year=2000, month=6, day=1),
        ],
        'strike_price': [
            1,
        ],
        'put_or_call': [
            'call',
        ],
        'volume': [
            6,
        ]
        }
    )

    assert np.all(result == expected)

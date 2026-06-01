import pandas as pd
from txf_mcp.features.patterns.deep_pit import DeepPit
from txf_mcp.features.patterns.high_point import HighPoint
from txf_mcp.features.patterns.low_point import LowPoint


def _bars(o, h, l, c):
    return pd.DataFrame({"open": o, "high": h, "low": l, "close": c,
                         "volume": [1] * len(o), "n": [1] * len(o)})


def test_deep_pit_detects_long_lower_wick_local_low():
    bars = _bars([100, 100, 100], [101, 101, 101], [99, 80, 99], [100, 99, 100])
    s = DeepPit().detect(bars)
    assert bool(s.iloc[1]) is True
    assert bool(s.iloc[0]) is False


def test_high_point_detects_local_max_close_upper_half():
    bars = _bars([100, 100, 100], [105, 120, 105], [95, 100, 95], [100, 118, 100])
    s = HighPoint(window=1).detect(bars)
    assert bool(s.iloc[1]) is True


def test_low_point_detects_local_min_close_lower_half():
    bars = _bars([100, 100, 100], [105, 100, 105], [95, 80, 95], [100, 82, 100])
    s = LowPoint(window=1).detect(bars)
    assert bool(s.iloc[1]) is True

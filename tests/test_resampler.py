import pandas as pd
from txf_mcp.klines.resampler import resample


def _ticks():
    dt = pd.to_datetime([
        "2026-05-29 09:00:00", "2026-05-29 09:00:30",
        "2026-05-29 09:01:10", "2026-05-29 09:01:50",
    ]).tz_localize("+08:00")
    return pd.DataFrame({
        "datetime": dt, "price": [100, 105, 110, 95], "volume": [2, 3, 1, 4],
        "is_auction": [False] * 4, "session": ["day"] * 4,
    })


def test_1min_ohlcv():
    bars = resample(_ticks(), "1min")
    assert len(bars) == 2
    first = bars.iloc[0]
    assert first["open"] == 100 and first["high"] == 105
    assert first["low"] == 100 and first["close"] == 105
    assert first["volume"] == 5 and first["n"] == 2


def test_volume_preserved_across_timeframes():
    t = _ticks()
    total = t["volume"].sum()
    for tf in ["1s", "1min", "5min"]:
        assert resample(t, tf)["volume"].sum() == total


def test_session_column_present():
    bars = resample(_ticks(), "5min")
    assert "session" in bars.columns

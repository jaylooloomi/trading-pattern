import pandas as pd
from txf_mcp.data.cleaner import clean_ticks


def _frame(prices, vols=None):
    n = len(prices)
    dt = pd.date_range("2026-05-29 09:00:00+08:00", periods=n, freq="s")
    return pd.DataFrame({
        "datetime": dt,
        "price": prices,
        "volume": vols or [1] * n,
        "is_auction": [False] * n,
        "expiry": ["202606"] * n,
    })


def test_drops_zero_and_negative_prices():
    df = clean_ticks(_frame([100, 0, -5, 101]))
    assert (df["price"] > 0).all()
    assert len(df) == 2


def test_sorted_by_datetime():
    df = _frame([1, 2, 3]).iloc[::-1].reset_index(drop=True)
    out = clean_ticks(df)
    assert out["datetime"].is_monotonic_increasing


def test_reports_filtered_count(capsys):
    clean_ticks(_frame([100, 0, 101]))
    assert "filtered" in capsys.readouterr().err.lower()

from pathlib import Path
from txf_mcp.data.loader import load_tx_ticks

FIXTURE = Path("tests/fixtures/TX_sample_2026_05_29.csv")


def test_returns_dataframe_with_expected_columns():
    df = load_tx_ticks(FIXTURE)
    assert list(df.columns) == ["datetime", "price", "volume", "is_auction", "expiry"]


def test_only_tx_near_month_no_spreads():
    df = load_tx_ticks(FIXTURE)
    assert df["expiry"].str.contains("/").sum() == 0
    assert df["expiry"].nunique() == 1


def test_volume_halved_and_integer():
    df = load_tx_ticks(FIXTURE)
    assert (df["volume"] >= 1).all()
    assert df["volume"].dtype.kind in ("i", "u")


def test_datetime_parsed_with_tz():
    df = load_tx_ticks(FIXTURE)
    assert df["datetime"].dt.tz is not None
    assert df["datetime"].dt.date.nunique() == 2


def test_auction_flag_detected():
    df = load_tx_ticks(FIXTURE)
    assert df["is_auction"].any()

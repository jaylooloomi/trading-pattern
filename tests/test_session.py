import pandas as pd
from txf_mcp.data.session import tag_session


def _row(ts):
    return pd.DataFrame({
        "datetime": pd.to_datetime([ts]).tz_localize("+08:00"),
        "price": [100], "volume": [1], "is_auction": [False], "expiry": ["202606"],
    })


def test_day_tick():
    out = tag_session(_row("2026-05-29 09:30:00"))
    assert out["session"].iloc[0] == "day"


def test_evening_night_tick():
    out = tag_session(_row("2026-05-28 15:30:00"))
    assert out["session"].iloc[0] == "night"


def test_post_midnight_night_tick():
    out = tag_session(_row("2026-05-29 02:00:00"))
    assert out["session"].iloc[0] == "night"


def test_filter_session():
    df = pd.concat([_row("2026-05-29 09:30:00"), _row("2026-05-28 15:30:00")], ignore_index=True)
    out = tag_session(df)
    assert (out[out["session"] == "day"]).shape[0] == 1

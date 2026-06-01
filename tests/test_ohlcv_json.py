import json
import pandas as pd
from txf_mcp.klines.ohlcv_json import write_ohlcv_json, read_ohlcv_json


def _bars():
    return pd.DataFrame({
        "datetime": pd.to_datetime(["2026-05-29 09:00:00"]).tz_localize("+08:00"),
        "open": [100], "high": [110], "low": [95], "close": [105],
        "volume": [5], "n": [2], "session": ["day"],
    })


def test_write_then_read_roundtrip(tmp_path):
    p = tmp_path / "TX_2026-05-29_1min.json"
    write_ohlcv_json(_bars(), p, product="TX", contract="202606",
                     trade_date="2026-05-29", timeframe="1min",
                     source_file="Daily_2026_05_29.csv")
    doc = json.loads(p.read_text(encoding="utf-8"))
    assert doc["meta"]["timeframe"] == "1min"
    assert doc["meta"]["bar_count"] == 1
    assert doc["meta"]["total_volume"] == 5
    bar = doc["bars"][0]
    assert bar["o"] == 100 and bar["h"] == 110 and bar["l"] == 95 and bar["c"] == 105
    assert bar["v"] == 5 and bar["n"] == 2 and bar["session"] == "day"


def test_read_returns_dataframe(tmp_path):
    p = tmp_path / "f.json"
    write_ohlcv_json(_bars(), p, product="TX", contract="202606",
                     trade_date="2026-05-29", timeframe="1min", source_file="x.csv")
    df = read_ohlcv_json(p)
    assert list(df.columns) == ["datetime", "open", "high", "low", "close", "volume", "n", "session"]
    assert df["close"].iloc[0] == 105

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import pandas as pd

_TPE = timezone(timedelta(hours=8))


def write_ohlcv_json(bars: pd.DataFrame, path, *, product, contract,
                     trade_date, timeframe, source_file) -> None:
    rows = []
    for _, r in bars.iterrows():
        rows.append({
            "t": r["datetime"].isoformat(),
            "session": r["session"],
            "o": int(r["open"]), "h": int(r["high"]),
            "l": int(r["low"]), "c": int(r["close"]),
            "v": int(r["volume"]), "n": int(r["n"]),
        })
    doc = {
        "meta": {
            "product": product, "contract": contract, "trade_date": trade_date,
            "timeframe": timeframe, "source_file": source_file,
            "generated_at": datetime.now(_TPE).isoformat(),
            "bar_count": len(rows),
            "total_volume": int(bars["volume"].sum()) if len(bars) else 0,
        },
        "bars": rows,
    }
    Path(path).write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")


def read_ohlcv_json(path) -> pd.DataFrame:
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    bars = doc["bars"]
    df = pd.DataFrame({
        "datetime": pd.to_datetime([b["t"] for b in bars]),
        "open": [b["o"] for b in bars], "high": [b["h"] for b in bars],
        "low": [b["l"] for b in bars], "close": [b["c"] for b in bars],
        "volume": [b["v"] for b in bars], "n": [b["n"] for b in bars],
        "session": [b["session"] for b in bars],
    })
    return df

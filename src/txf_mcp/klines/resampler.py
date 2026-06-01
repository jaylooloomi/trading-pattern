import pandas as pd
from ..constants import RESAMPLE_RULE


def resample(ticks: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Resample tick frame into OHLCV bars for the given timeframe.

    Output columns: datetime (bar start), open, high, low, close,
    volume, n (tick count), session. Empty bars are dropped.
    """
    rule = RESAMPLE_RULE[timeframe]
    df = ticks.set_index("datetime")
    agg = df["price"].resample(rule, label="left", closed="left").ohlc()
    agg["volume"] = df["volume"].resample(rule, label="left", closed="left").sum()
    agg["n"] = df["price"].resample(rule, label="left", closed="left").count()
    agg["session"] = df["session"].resample(rule, label="left", closed="left").first()
    agg = agg.dropna(subset=["open"]).reset_index()
    agg["volume"] = agg["volume"].astype(int)
    agg["n"] = agg["n"].astype(int)
    for col in ["open", "high", "low", "close"]:
        agg[col] = agg[col].astype(int)
    return agg

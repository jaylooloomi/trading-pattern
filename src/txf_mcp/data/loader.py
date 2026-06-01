from pathlib import Path
import pandas as pd
from ..constants import PRODUCT, TZ

_COLS = ["trade_date", "product", "expiry", "trade_time",
         "price", "volume_bs", "near", "far", "auction"]


def load_tx_ticks(csv_path: str | Path) -> pd.DataFrame:
    """Load TAIFEX daily CSV, return cleaned TX near-month tick frame.

    Columns out: datetime (tz-aware), price (int), volume (int, B+S/2),
    is_auction (bool), expiry (str).
    """
    raw = pd.read_csv(
        csv_path, encoding="big5", names=_COLS, header=0,
        dtype=str, skipinitialspace=True,
    )
    for col in raw.columns:
        raw[col] = raw[col].str.strip()

    tx = raw[raw["product"] == PRODUCT].copy()
    tx = tx[~tx["expiry"].str.contains("/", na=False)]
    near = tx["expiry"].value_counts().idxmax()
    tx = tx[tx["expiry"] == near].copy()

    dt = pd.to_datetime(
        tx["trade_date"] + tx["trade_time"].str.zfill(6),
        format="%Y%m%d%H%M%S",
    ).dt.tz_localize(TZ)

    out = pd.DataFrame({
        "datetime": dt,
        "price": tx["price"].astype(int),
        "volume": (tx["volume_bs"].astype(int) // 2).clip(lower=1),
        "is_auction": tx["auction"].fillna("").str.contains(r"\*"),
        "expiry": near,
    })
    return out.reset_index(drop=True)

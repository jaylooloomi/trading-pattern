import sys
import pandas as pd


def clean_ticks(df: pd.DataFrame) -> pd.DataFrame:
    """Sort by time, drop duplicate rows, filter abnormal prices (<=0)."""
    before = len(df)
    out = df[df["price"] > 0].copy()
    out = out.drop_duplicates()
    out = out.sort_values("datetime", kind="stable").reset_index(drop=True)
    dropped = before - len(out)
    if dropped:
        print(f"cleaner: filtered {dropped} abnormal/duplicate ticks", file=sys.stderr)
    return out

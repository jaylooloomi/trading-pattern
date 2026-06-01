import datetime as _dt
import pandas as pd

_DAY_START = _dt.time(8, 45)
_DAY_END = _dt.time(13, 45)


def tag_session(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'session' column: 'day' for 08:45-13:45, else 'night'."""
    out = df.copy()
    tod = out["datetime"].dt.time
    is_day = (tod >= _DAY_START) & (tod <= _DAY_END)
    out["session"] = is_day.map({True: "day", False: "night"})
    return out

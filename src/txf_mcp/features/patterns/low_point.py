import pandas as pd
from ..base import FeaturePattern


class LowPoint(FeaturePattern):
    name = "low_point"
    category = "down"

    def __init__(self, window: int = 3):
        self.window = window

    def detect(self, klines: pd.DataFrame) -> pd.Series:
        w = self.window
        rolling_min = klines["low"].rolling(2 * w + 1, center=True, min_periods=1).min()
        is_local_min = klines["low"] <= rolling_min
        mid = (klines["high"] + klines["low"]) / 2
        close_lower = klines["close"] <= mid
        return (is_local_min & close_lower).fillna(False)

import pandas as pd
from ..base import FeaturePattern


class HighPoint(FeaturePattern):
    name = "high_point"
    category = "up"

    def __init__(self, window: int = 3):
        self.window = window

    def detect(self, klines: pd.DataFrame) -> pd.Series:
        w = self.window
        rolling_max = klines["high"].rolling(2 * w + 1, center=True, min_periods=1).max()
        is_local_max = klines["high"] >= rolling_max
        mid = (klines["high"] + klines["low"]) / 2
        close_upper = klines["close"] >= mid
        return (is_local_max & close_upper).fillna(False)

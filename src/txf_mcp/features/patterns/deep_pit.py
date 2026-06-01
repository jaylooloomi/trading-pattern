import pandas as pd
from ..base import FeaturePattern


class DeepPit(FeaturePattern):
    name = "deep_pit"
    category = "reversal"

    def __init__(self, wick_body_ratio: float = 2.0):
        self.wick_body_ratio = wick_body_ratio

    def detect(self, klines: pd.DataFrame) -> pd.Series:
        body = (klines["close"] - klines["open"]).abs()
        body_low = klines[["open", "close"]].min(axis=1)
        lower_wick = body_low - klines["low"]
        long_wick = lower_wick > (body.clip(lower=1) * self.wick_body_ratio)
        local_low = (klines["low"] < klines["low"].shift(1)) & \
                    (klines["low"] < klines["low"].shift(-1))
        return (long_wick & local_low).fillna(False)

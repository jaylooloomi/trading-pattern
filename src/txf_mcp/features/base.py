from abc import ABC, abstractmethod
import pandas as pd


class FeaturePattern(ABC):
    name: str = ""
    category: str = "reversal"  # "up" | "down" | "reversal"

    @abstractmethod
    def detect(self, klines: pd.DataFrame) -> pd.Series:
        """Return a bool Series aligned to klines (same length).
        The same detect() must apply to any timeframe (fractal assumption)."""

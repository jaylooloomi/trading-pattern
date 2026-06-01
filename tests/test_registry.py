import pandas as pd
from txf_mcp.features.registry import discover_patterns
from txf_mcp.features.base import FeaturePattern


def test_discovers_three_example_patterns():
    patterns = discover_patterns()
    names = {p.name for p in patterns}
    assert {"deep_pit", "high_point", "low_point"} <= names


def test_patterns_are_feature_instances():
    for p in discover_patterns():
        assert isinstance(p, FeaturePattern)
        assert p.category in ("up", "down", "reversal")


def test_detect_returns_bool_series_same_length():
    bars = pd.DataFrame({
        "open": [100, 101, 102], "high": [105, 106, 103],
        "low": [95, 96, 90], "close": [104, 97, 102],
        "volume": [1, 1, 1], "n": [1, 1, 1],
    })
    for p in discover_patterns():
        s = p.detect(bars)
        assert len(s) == len(bars)
        assert s.dtype == bool

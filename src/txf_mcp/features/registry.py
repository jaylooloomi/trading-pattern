import importlib
import pkgutil
from . import patterns as _patterns_pkg
from .base import FeaturePattern


def discover_patterns() -> list[FeaturePattern]:
    """Import every module in features/patterns/ and instantiate each
    FeaturePattern subclass found."""
    found: list[FeaturePattern] = []
    for info in pkgutil.iter_modules(_patterns_pkg.__path__):
        mod = importlib.import_module(f"{_patterns_pkg.__name__}.{info.name}")
        for attr in vars(mod).values():
            if (isinstance(attr, type) and issubclass(attr, FeaturePattern)
                    and attr is not FeaturePattern):
                found.append(attr())
    return found

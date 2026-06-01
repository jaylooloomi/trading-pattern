# 新增特徵指南

特徵採插件式設計：新增一個特徵只需在 `src/txf_mcp/features/patterns/` 放一個檔案，
registry 會自動掃描載入，**不需要修改任何核心程式碼**。

## 步驟

1. 在 `src/txf_mcp/features/patterns/` 新增 `<your_feature>.py`
2. 繼承 `FeaturePattern`，設定 `name` 與 `category`
3. 實作 `detect(klines) -> pd.Series`，回傳與 `klines` 等長的 bool Series

```python
# src/txf_mcp/features/patterns/my_pattern.py
import pandas as pd
from ..base import FeaturePattern


class MyPattern(FeaturePattern):
    name = "my_pattern"
    category = "reversal"   # "up" | "down" | "reversal"

    def detect(self, klines: pd.DataFrame) -> pd.Series:
        # klines 欄位：open, high, low, close, volume, n, session
        body = (klines["close"] - klines["open"]).abs()
        return (body > body.mean()).fillna(False)
```

## 重要約束

- **回傳型別**：必須是 `bool` dtype 的 `pd.Series`，長度等於輸入 `klines`
- **碎形假設**：同一份 `detect()` 必須能套用到任何時間框架（1s 到 15min），
  不要寫死特定框架的根數假設；用相對關係（例如 rolling window）而非絕對時間
- **向量化**：用 pandas/numpy 運算，避免 Python for-loop（效能需求）
- **命名唯一**：`name` 不可與既有特徵重複

## 驗證

新增後執行測試確認 registry 能載入：

```bash
uv run pytest tests/test_registry.py -v
```

`discover_patterns()` 會自動包含你的新特徵，`analyze_txf_day` 等工具也會自動套用。

## 替換範例特徵

內附的 `deep_pit` / `high_point` / `low_point` 是**佔位範例**。
要換成你自己的量化定義時，直接編輯對應的 `patterns/*.py` 即可，介面不變。

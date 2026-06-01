# Trading Pattern — 台指期特徵分析 MCP Server

一個 MCP (Model Context Protocol) Server，把台指期（TX）的逐筆成交資料轉成多框架 OHLCV，自動識別交易形態特徵，並提供給 Claude / 其他 LLM 分析查詢。

## 功能

- **資料下載**：依日期從台灣期交所（TAIFEX）下載逐筆成交 zip 並快取
- **6 框架 OHLCV**：逐秒、1/3/5/10/15 分鐘 K，輸出為 JSON 檔
- **特徵識別**：可擴充的形態演算法（內附深坑K / 高點K / 低點K 範例）
- **多框架共振**：不同時間框架同類特徵同時出現的共振分數
- **回測驗證**：特徵出現後續走勢的勝率與報酬統計
- **MCP 介面**：4 個工具供 LLM 查詢

## 安裝

需要 [uv](https://docs.astral.sh/uv/) 與 Python 3.10+。

```bash
uv sync --extra dev
```

## 使用

### 1. 產生 OHLCV JSON

從已下載的 CSV 產生 6 個框架的 JSON（輸出到 `data/ohlcv/`）：

```python
from txf_mcp.pipeline import build_ohlcv_from_csv
build_ohlcv_from_csv("tests/fixtures/TX_sample_2026_05_29.csv", "2026-05-29")
```

或直接從期交所下載當日資料再轉換：

```python
from txf_mcp.data.downloader import download
from txf_mcp.pipeline import build_ohlcv_from_csv

csv_path = download("2026-05-29")              # 抓 zip → 解壓 → data/raw/
build_ohlcv_from_csv(csv_path, "2026-05-29")   # → data/ohlcv/*.json
```

每個交易日產生 6 個檔：`TX_2026-05-29_{1s,1min,3min,5min,10min,15min}.json`。

### 2. 啟動 MCP Server

```bash
uv run python -m txf_mcp.mcp_server.server
```

### 3. Claude Desktop 設定

在 `claude_desktop_config.json` 加入：

```json
{
  "mcpServers": {
    "txf-feature-analysis": {
      "command": "uv",
      "args": ["--directory", "D:/git/trading-pattern", "run", "python", "-m", "txf_mcp.mcp_server.server"]
    }
  }
}
```

## MCP 工具

| 工具 | 用途 |
|---|---|
| `analyze_txf_day(date, timeframes, session)` | 指定日期的完整特徵序列 + 多框架共振 |
| `query_feature_statistics(feature, timeframe, date_range, lookforward_bars)` | 特徵出現後的後續走勢統計 |
| `compare_days(target_date, compare_dates, timeframe)` | 多日特徵序列相似度（數值分數） |
| `list_available_dates()` | 列出本地快取中可查詢的日期 |

## OHLCV JSON 格式

```json
{
  "meta": {
    "product": "TX", "contract": "202606", "trade_date": "2026-05-29",
    "timeframe": "1min", "bar_count": 300, "total_volume": 95423
  },
  "bars": [
    {"t": "2026-05-28T15:00:00+08:00", "session": "night",
     "o": 43964, "h": 43970, "l": 43958, "c": 43965, "v": 1234, "n": 56}
  ]
}
```

- `t` K棒起始時間（ISO 8601，夜盤跨午夜自然遞增）；`session` 日盤/夜盤
- `o/h/l/c` 開高低收；`v` 成交量（已 ÷2 真實口數）；`n` tick 筆數

## 資料來源說明（TAIFEX 實測）

- 商品代號為 **`TX`**（大台），編碼 **Big5**，時間精度到秒
- 成交量是 **B+S 雙邊合計**，已自動 ÷2
- 自動濾掉跨月價差單、只取近月合約
- 盤別：夜盤前一日 15:00 → 隔日 05:00（跨午夜）；日盤 08:45–13:45

## 新增特徵

見 [docs/adding_features.md](docs/adding_features.md)。

## 測試

```bash
uv run pytest
```

## 開發文件

- 設計規格：[docs/superpowers/specs/2026-06-02-txf-feature-mcp-design.md](docs/superpowers/specs/2026-06-02-txf-feature-mcp-design.md)
- 實作計畫：[docs/superpowers/plans/2026-06-02-txf-feature-mcp.md](docs/superpowers/plans/2026-06-02-txf-feature-mcp.md)

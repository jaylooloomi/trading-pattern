import urllib.request
import zipfile
from pathlib import Path

_BASE = ("https://www.taifex.com.tw/file/taifex/Dailydownload/"
         "DailydownloadCSV/Daily_{y}_{m}_{d}.zip")


def build_url(trade_date: str) -> str:
    """trade_date: 'YYYY-MM-DD' -> TAIFEX daily zip URL."""
    y, m, d = trade_date.split("-")
    return _BASE.format(y=y, m=m, d=d)


def extract_csv(zip_path, dest_dir) -> str:
    dest = Path(dest_dir)
    with zipfile.ZipFile(zip_path) as z:
        name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
        z.extract(name, dest)
    return str(dest / name)


def download(trade_date: str, cache_dir="data/raw") -> str:
    """Download (if not cached) and extract the daily CSV. Returns CSV path."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    csv_path = cache / f"Daily_{trade_date.replace('-', '_')}.csv"
    if csv_path.exists():
        return str(csv_path)
    zip_path = cache / f"Daily_{trade_date.replace('-', '_')}.zip"
    req = urllib.request.Request(build_url(trade_date),
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(zip_path, "wb") as f:
        f.write(resp.read())
    return extract_csv(zip_path, cache)

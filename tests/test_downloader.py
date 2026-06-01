import zipfile
from pathlib import Path
from txf_mcp.data.downloader import build_url, extract_csv


def test_build_url():
    url = build_url("2026-05-29")
    assert url == ("https://www.taifex.com.tw/file/taifex/Dailydownload/"
                   "DailydownloadCSV/Daily_2026_05_29.zip")


def test_extract_csv(tmp_path):
    csv = tmp_path / "Daily_2026_05_29.csv"
    csv.write_text("a,b\n1,2\n", encoding="utf-8")
    zpath = tmp_path / "Daily_2026_05_29.zip"
    with zipfile.ZipFile(zpath, "w") as z:
        z.write(csv, arcname="Daily_2026_05_29.csv")
    csv.unlink()
    out = extract_csv(zpath, tmp_path)
    assert Path(out).exists() and Path(out).suffix == ".csv"

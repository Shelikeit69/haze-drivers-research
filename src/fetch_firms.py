"""Download NASA FIRMS MODIS active-fire detections, 1 Aug - 31 Oct, one box covering
Sumatra and Kalimantan (west 100, south -5, east 116.5, north 2.3).

- 2001-2025: MODIS_SP (standard processing, Terra + Aqua)
- 2026: MODIS_NRT (near real time; SP not yet available), 1 Aug - 15 Oct

The MAP_KEY is read from the environment variable FIRMS_MAP_KEY and is never written
to disk or printed. Raw CSV responses are saved unchanged under data/raw/firms/.
Classification into islands happens later in analyse_r4.py, not here.

Usage: FIRMS_MAP_KEY=... python src/fetch_firms.py data/raw/firms
"""
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date, timedelta

KEY = os.environ.get("FIRMS_MAP_KEY")
if not KEY:
    sys.exit("Set FIRMS_MAP_KEY in the environment.")
OUT = sys.argv[1] if len(sys.argv) > 1 else "data/raw/firms"
os.makedirs(OUT, exist_ok=True)

BOX = "100,-5,116.5,2.3"
BASE = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
DAYS = 5  # API maximum per request


def get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                body = r.read()
            if body.startswith(b"latitude"):
                return body
            msg = body[:120].decode(errors="replace")
        except Exception as e:  # noqa: BLE001
            msg = type(e).__name__  # never print the URL (it contains the key)
        wait = 60 * (i + 1)
        print(f"  retry in {wait}s: {msg}", flush=True)
        time.sleep(wait)
    raise RuntimeError("FIRMS request failed repeatedly")


def run(source, year, start, end):
    d = start
    while d <= end:
        n = min(DAYS, (end - d).days + 1)
        path = os.path.join(OUT, f"{source}_{d.isoformat()}_{n}d.csv")
        if not os.path.exists(path):
            body = get(f"{BASE}/{KEY}/{source}/{BOX}/{n}/{d.isoformat()}")
            with open(path, "wb") as f:
                f.write(body)
            time.sleep(1)
        d += timedelta(days=n)


if __name__ == "__main__":
    for y in range(2001, 2026):
        run("MODIS_SP", y, date(y, 8, 1), date(y, 10, 31))
        print("MODIS_SP", y, flush=True)
    run("MODIS_NRT", 2026, date(2026, 8, 1), date(2026, 10, 15))
    print("MODIS_NRT 2026\ndone", flush=True)

"""Download raw data for the El Nino vs haze study.

1. ERA5 daily mean sea-level pressure at Darwin and Tahiti (for SOI), 1950 to now.
2. ERA5 daily precipitation at six fire-region points in Sumatra and Kalimantan.
3. NEA hourly PSI / PM2.5 readings (national), Aug-Oct 2016-2026.

All raw responses are saved unchanged under data/raw/.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import date, timedelta, datetime, timezone

OUT = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
os.makedirs(OUT, exist_ok=True)

TODAY_UTC = datetime.now(timezone.utc).date()
END = (TODAY_UTC - timedelta(days=6)).isoformat()  # ERA5 has a few days of lag


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:  # NEA: no data for this date; keep the error body as the record
                return e.read()
            wait = 30 * (i + 1)
            print(f"  error {e}; retry in {wait}s", flush=True)
            time.sleep(wait)
        except Exception as e:  # noqa: BLE001
            wait = 30 * (i + 1)
            print(f"  error {e}; retry in {wait}s", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"failed: {url}")


ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"

POINTS = {
    # SOI stations
    "darwin": (-12.46, 130.84),
    "tahiti": (-17.53, -149.57),
    # fire regions (approximate centres of main peat/fire provinces)
    "riau": (0.50, 101.50),
    "jambi": (-1.60, 103.60),
    "south_sumatra": (-3.00, 104.80),
    "west_kalimantan": (-0.50, 109.50),
    "central_kalimantan": (-2.20, 113.90),
    "south_kalimantan": (-3.30, 114.60),
}


def fetch_era5():
    for name, (lat, lon) in POINTS.items():
        path = os.path.join(OUT, f"era5_{name}.json")
        if os.path.exists(path):
            print("skip", name)
            continue
        url = (f"{ARCHIVE}?latitude={lat}&longitude={lon}&start_date=1950-01-01"
               f"&end_date={END}&daily=pressure_msl_mean,precipitation_sum&timezone=UTC")
        print("era5", name, flush=True)
        raw = get(url)
        with open(path, "wb") as f:
            f.write(raw)
        time.sleep(5)


PSI = "https://api-open.data.gov.sg/v2/real-time/api/psi?date={}"


def fetch_psi():
    d_out = os.path.join(OUT, "psi")
    os.makedirs(d_out, exist_ok=True)
    for year in range(2016, 2027):
        d = date(year, 8, 1)
        stop = min(date(year, 10, 31), TODAY_UTC - timedelta(days=1))
        while d <= stop:
            path = os.path.join(d_out, f"{d.isoformat()}.json")
            if not os.path.exists(path):
                raw = get(PSI.format(d.isoformat()))
                with open(path, "wb") as f:
                    f.write(raw)
                time.sleep(0.3)
            d += timedelta(days=1)
        print("psi", year, flush=True)


if __name__ == "__main__":
    fetch_era5()
    fetch_psi()
    print("done")

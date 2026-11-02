"""Plan v2: extend the FIRMS MODIS_SP download to 1 Jun - 31 Jan, 2002-2025.

v1 already holds 1 Aug - 31 Oct for every year (src/fetch_firms.py). This script adds
1 Jun - 31 Jul and 1 Nov - 31 Jan (of the next year), same box and same file naming,
so events near the edges of the Jul-Dec season are not cut off.

The MAP_KEY is read from FIRMS_MAP_KEY and is never written to disk or printed.

Files go to a separate folder (data/raw/firms_v2) so the v1 inputs in data/raw/firms,
which src/analyse_r4.py reads in full, stay unchanged.

Usage: FIRMS_MAP_KEY=... python src/fetch_firms_v2.py data/raw/firms_v2
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
import fetch_firms as f1  # noqa: E402  (reuses the v1 request and retry logic)

if __name__ == "__main__":
    for y in range(2002, 2026):
        f1.run("MODIS_SP", y, date(y, 6, 1), date(y, 7, 31))
        f1.run("MODIS_SP", y, date(y, 11, 1), date(y + 1, 1, 31))
        print("MODIS_SP", y, flush=True)
    print("done", flush=True)

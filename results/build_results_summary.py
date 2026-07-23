#!/usr/bin/env python3
"""Aggregate solved scenarios into results/RESULTS_SUMMARY.csv.

Scans both passes: outputs_<name>/ (p025) and outputs_p001_<name>/ (p001).
One row per (scenario, pass). total_cost_npv in $; solved_at in HST.
The 0.1% value supersedes the 0.25% one for the same cell when present.
"""
import csv, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
REPO = Path(__file__).resolve().parent.parent    # portable: repo root from script
HST = ZoneInfo("Pacific/Honolulu")
# hard cells (docs/HARD_CELLS.md) solve at 0.0015 unless the retry pass
# confirmed 0.001 (marker .confirmed_p001 written by solve/promote_retries.py)
HARD = {c.strip("- `") for c in
        (REPO / "docs" / "HARD_CELLS.md").read_text().splitlines()
        if c.startswith("- `")}
rows = {}
for tc in REPO.glob("outputs_*/total_cost.txt"):
    d = tc.parent.name.replace("outputs_", "")
    if d.startswith(("p001retry_", "p0015bak_")):
        continue  # in-flight retries and 0.15% archives are not result rows
    p001 = d.startswith("p001_")
    name = d[len("p001_"):] if p001 else d
    cost = float(tc.read_text().strip())
    mt = datetime.datetime.fromtimestamp(tc.stat().st_mtime, HST).strftime("%Y-%m-%d %H:%M")
    if p001:
        confirmed = (tc.parent / ".confirmed_p001").exists()
        gap = "0.001" if (confirmed or name not in HARD) else "0.0015"
    else:
        gap = "0.0025"
    rows[(name, "p001" if p001 else "p025")] = dict(
        scenario=name, total_cost_npv=f"{cost:.2f}",
        mipgap=gap, solved_at_hst=mt)
out = REPO / "results" / "RESULTS_SUMMARY.csv"
recs = [rows[k] for k in sorted(rows)]
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["scenario","total_cost_npv","mipgap","solved_at_hst"])
    w.writeheader(); w.writerows(recs)
n01 = sum(1 for k in rows if k[1]=="p001")
print(f"{out.name}: {len(recs)} rows ({n01} at 0.1%, {len(recs)-n01} at 0.25%)")

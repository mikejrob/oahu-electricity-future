#!/usr/bin/env python3
"""Aggregate solved scenarios into results/RESULTS_SUMMARY.csv.

Covers the report-basis fleet: the corrected distributed-solar families
(nlv2b / nlv2s / nlv2a) on the four market oil paths (market 10th
percentile, Brent futures, EIA reference, market 90th percentile), one row
per scenario at its best available tolerance:

    R010_outputs_<name>  (0.1%)  >  R0015_outputs_<name>  (0.15%)
                                 >  outputs_<name>        (0.25%)

Legacy gross-load families and archived AEO oil paths are excluded, the
same policy as report/figures/make_report_figures.py and the explorer
extractor — mixing netting conventions or oil vintages in one table
silently corrupts comparisons. total_cost_npv in $; solved_at in HST from
the total_cost.txt mtime of the winning pass.
"""
import csv
import datetime
import re
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
HST = ZoneInfo("Pacific/Honolulu")
OIL = ("lowbrent", "futbrent", "refbrent", "highbrent")

names = set()
for p in REPO.iterdir():
    m = re.match(r"^(R010_|R0015_)?outputs_(nlv2[bsa]_.+)$", p.name)
    if m and (p / "total_cost.txt").exists():
        names.add(m.group(2))
names = {n for n in names if any(f"_{o}" in n for o in OIL)}

rows = []
for name in sorted(names):
    for pre, gap in (("R010_outputs_", "0.001"), ("R0015_outputs_", "0.0015"),
                     ("outputs_", "0.0025")):
        tc = REPO / f"{pre}{name}" / "total_cost.txt"
        if tc.exists():
            ts = datetime.datetime.fromtimestamp(tc.stat().st_mtime, HST)
            rows.append({
                "scenario": name,
                "total_cost_npv": f"{float(tc.read_text()):.2f}",
                "mipgap": gap,
                "solved_at_hst": ts.strftime("%Y-%m-%d %H:%M"),
            })
            break

out = REPO / "results" / "RESULTS_SUMMARY.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["scenario", "total_cost_npv", "mipgap",
                                      "solved_at_hst"], lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
n010 = sum(1 for r in rows if r["mipgap"] == "0.001")
print(f"RESULTS_SUMMARY.csv: {len(rows)} scenarios ({n010} at 0.1%)")

#!/usr/bin/env python3
"""Build results/CORRECTION_DELTAS.csv: old vs new cost for every published cell.

"Old" is the pre-correction fleet preserved under AUDITSTALE_ prefixes
(September 2026 input corrections: battery netting in the nlv2* loads, EGS
alias-file storage credits, advsolar credit sync — docs/CORRECTIONS.md).
"New" is the re-solved fleet. Each row compares the two solutions AT THE
SAME REQUESTED TOLERANCE — the finest tier solved on both sides:

    R010_outputs_<name>  (0.1%)  >  R0015_outputs_<name>  (0.15%)
                                 >  outputs_<name>        (0.25%)

Comparing across tiers would fold refinement movement into the correction
delta; at a matched tier the difference isolates the input change up to
twice the tolerance. The published-cell register is the set of
AUDITSTALE_R010_outputs_* directories (the 513 cells the report used).

Run after the re-solve fleet lands; re-run after R010 refinements to move
matched_gap from 0.0025 to 0.001. Cells with no new solve yet appear with
empty new columns so the gap is visible, and the exit status is nonzero
until every cell has a matched-tier comparison.
"""
import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TIERS = (("R010_", "0.001"), ("R0015_", "0.0015"), ("", "0.0025"))


def cost(path):
    tc = path / "total_cost.txt"
    return float(tc.read_text()) if tc.exists() else None


published = sorted(
    p.name[len("AUDITSTALE_R010_outputs_"):]
    for p in REPO.iterdir()
    if p.name.startswith("AUDITSTALE_R010_outputs_")
)
if not published:
    sys.exit("no AUDITSTALE_R010_outputs_* directories — nothing to compare")

rows, unmatched = [], []
for name in published:
    row = {"scenario": name, "matched_gap": "", "old_npv": "", "new_npv": "",
           "delta_usd": "", "delta_pct": ""}
    for pre, gap in TIERS:
        old = cost(REPO / f"AUDITSTALE_{pre}outputs_{name}")
        new = cost(REPO / f"{pre}outputs_{name}")
        if old is not None and new is not None:
            row.update({
                "matched_gap": gap,
                "old_npv": f"{old:.2f}",
                "new_npv": f"{new:.2f}",
                "delta_usd": f"{new - old:.2f}",
                "delta_pct": f"{(new - old) / old * 100:.4f}",
            })
            break
    if not row["matched_gap"]:
        unmatched.append(name)
    rows.append(row)

out = REPO / "results" / "CORRECTION_DELTAS.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["scenario", "matched_gap", "old_npv",
                                      "new_npv", "delta_usd", "delta_pct"],
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

matched = [r for r in rows if r["matched_gap"]]
at010 = sum(1 for r in matched if r["matched_gap"] == "0.001")
pcts = sorted(float(r["delta_pct"]) for r in matched)
if pcts:
    med = pcts[len(pcts) // 2]
    print(f"CORRECTION_DELTAS.csv: {len(matched)}/{len(rows)} cells matched "
          f"({at010} at 0.1%); delta_pct min {pcts[0]:+.2f} / median {med:+.2f} "
          f"/ max {pcts[-1]:+.2f}")
if unmatched:
    print(f"UNMATCHED ({len(unmatched)}): " + ", ".join(unmatched[:10])
          + (" ..." if len(unmatched) > 10 else ""))
    sys.exit(1)

#!/usr/bin/env python3
"""Audit (and optionally quarantine) refinement dirs invalidated by the JERA
part-load fix.

Every cell carrying the JERA plant was re-solved on the CEMS-derived fuel
curve (issue #2, sources/epa_cems/), writing to its 0.25% `outputs_` dir.
Any `R010_`/`R0015_` dir for the same cell still holds a pre-fix solution,
and the analysis helpers prefer those prefixes — so they must be moved
aside or every downstream number silently reverts to the old curve.

  python3 analysis/audit_stale_jera_refinements.py            # report only
  python3 analysis/audit_stale_jera_refinements.py --quarantine

Quarantine renames `R010_x` -> `STALE_R010_x` (reversible; nothing is
deleted). Re-running the 0.1% refinement pass on the new inputs is what
eventually replaces them.
"""
import argparse
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BATCHES = sorted(REPO.glob("scenarios/scenarios_jera_hr_b*.txt"))


def cells():
    out = []
    for f in BATCHES:
        for line in open(f):
            m = re.search(r"--outputs-dir (\S+)", line)
            if m:
                out.append((m.group(1), f.stat().st_mtime))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quarantine", action="store_true",
                    help="rename stale refinement dirs to STALE_*")
    args = ap.parse_args()

    resolved, pending, stale, held = [], [], [], []
    for od, list_mtime in cells():
        tc = REPO / od / "total_cost.txt"
        done = tc.exists() and tc.stat().st_mtime > list_mtime
        (resolved if done else pending).append(od)
        for pre in ("R010_", "R0015_"):
            d = REPO / (pre + od)
            if (d / "total_cost.txt").exists():
                # a still-solving cell warm-starts from its own stale dir,
                # so hold those back until that cell lands
                (stale if done else held).append(pre + od)

    print(f"JERA-carrying cells: {len(resolved) + len(pending)}")
    print(f"  re-solved on the new curve: {len(resolved)}")
    print(f"  still pending:              {len(pending)}")
    print(f"stale refinement dirs (pre-fix results that would shadow them): "
          f"{len(stale)}")
    for d in stale[:10]:
        print(f"    {d}")
    if len(stale) > 10:
        print(f"    ... and {len(stale) - 10} more")

    if held:
        print(f"held back (their cell is still solving and warm-starts from "
              f"them): {len(held)}")
    if args.quarantine:
        for d in stale:
            os.rename(REPO / d, REPO / ("STALE_" + d))
        print(f"\nquarantined {len(stale)} dirs (STALE_ prefix; reversible)")
        if held:
            print(f"{len(held)} left in place; re-run once those cells land")
    elif stale:
        print("\n(report only; pass --quarantine to move these aside)")


if __name__ == "__main__":
    main()

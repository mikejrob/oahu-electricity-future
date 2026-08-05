#!/usr/bin/env python3
"""Assemble the plan price-tag table: cost AND emissions per plan cell.

For each solved plan cell and its same-family, same-premium least-cost
reference: total system cost (PV 2027, 2024$), the price tag (delta),
cumulative 2027-2050 combustion CO2 (period-weighted, the Section 4.9
basis), the emissions delta, and for LNG cells the total LNG imports
(MMBtu) so the A.10 upstream-methane thresholds can be applied.

--design selects which quota revision's cells to read, so the tags can be
compared across revisions instead of the script silently following whichever
directories happen to exist:

  floors      the original floors-only cells. DISCARDED -- they overshoot the
              plans' utility solar 2.10x in 2045-2050 (audit_plan_mix_fidelity)
  windband    usolar and combined wind banded 0.98-1.02, offshore floored
  firmfloor   floors only, with the plan's firm clean energy (biofuel +
              hydrogen) floored 2045-2050

The reference cells are least-cost solves and do not vary by design. Every run
prints the design and the directories it actually read, because "which cells
did this number come from" is the question that keeps costing us.

Run from the repository root:
  python3 analysis/assemble_plan_price_tags.py --design firmfloor
"""
import argparse
import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
YRS = {2027: 3, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 5}
DESIGNS = ("hybrid", "firmfloor", "windband", "floors")

CELLS = [
    # (label, plan cell dir, reference dir)
    ("IGP land-constrained @1.2x", "outputs_nlv2a_plan_igp_pref_refbrent",
     "R010_outputs_nlv2a_C4_NOTHERMAL_refbrent"),
    ("IGP land-constrained @1.7x", "outputs_nlv2a_plan_igp_pref_pv17_refbrent",
     "outputs_nlv2a_be_pv17_C4_NOTHERMAL_refbrent"),
    ("IGP base @1.2x", "outputs_nlv2b_plan_igp_alt_refbrent",
     "R010_outputs_nlv2b_C4_NOTHERMAL_refbrent"),
    ("IGP base @1.7x", "outputs_nlv2b_plan_igp_alt_pv17_refbrent",
     "R010_outputs_nlv2b_be_pv17_C4_NOTHERMAL_refbrent"),
    ("HSEO oil @1.2x", "outputs_nlv2s_plan_hseo_oil_refbrent",
     "R010_outputs_nlv2s_C4_NOTHERMAL_refbrent"),
    ("HSEO oil @1.7x", "outputs_nlv2s_plan_hseo_oil_pv17_refbrent",
     "R010_outputs_nlv2s_be_pv17_C4_NOTHERMAL_refbrent"),
    ("HSEO LNG @1.2x", "outputs_nlv2s_plan_hseo_lng_refbrent",
     "R010_outputs_nlv2s_C4_NOTHERMAL_refbrent"),
    ("HSEO LNG @1.7x", "outputs_nlv2s_plan_hseo_lng_pv17_refbrent",
     "R010_outputs_nlv2s_be_pv17_C4_NOTHERMAL_refbrent"),
]


def best(dirname):
    for pre in ("R010_", "R0015_", ""):
        d = REPO / (pre + dirname.replace("R010_", "").replace("R0015_", ""))
        if (d / "total_cost.txt").exists():
            return d
    return None


def cost_bn(d):
    return float((d / "total_cost.txt").read_text()) / 1e9


def cum_co2_mt(d):
    tot = 0.0
    for r in csv.DictReader(open(d / "dispatch_annual_summary.csv")):
        p = int(r["period"])
        tot += float(r["DispatchEmissions_tCO2_per_typical_yr"] or 0) * YRS[p]
    return tot / 1e6


def lng_mmbtu(d):
    f = d / "ConsumeFuelTier.csv"
    if not f.exists():
        return 0.0
    tot = 0.0
    rd = csv.reader(open(f))
    next(rd)
    for row in rd:
        if any("LNG" in str(v) for v in row[:-1]):
            per = next((int(v) for v in row if v.isdigit() and len(v) == 4), None)
            if per in YRS:
                tot += float(row[-1]) * YRS[per]
    return tot


def for_design(plan_dir, design):
    """Insert the revision tag ahead of the oil-path suffix."""
    if design == "floors":
        return plan_dir
    return re.sub(r"_(refbrent|lowbrent|futbrent|highbrent)$",
                  rf"_{design}_\1", plan_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", choices=DESIGNS, default="firmfloor")
    args = ap.parse_args()

    print(f"design: {args.design}")
    print(f"{'cell':38s} {'plan $B':>8} {'ref $B':>8} {'tag $B':>8} "
          f"{'plan Mt':>8} {'ref Mt':>7} {'dMt':>6} {'LNG MMMBtu':>10}")
    read = []
    for label, plan, ref in CELLS:
        plan = for_design(plan, args.design)
        pd, rd = best(plan), best(ref)
        if pd is None or rd is None:
            print(f"{label:38s}   [pending: "
                  f"{plan if pd is None else ref}]")
            continue
        read.append((pd.name, rd.name))
        pc, rc = cost_bn(pd), cost_bn(rd)
        pe, re_ = cum_co2_mt(pd), cum_co2_mt(rd)
        lng = lng_mmbtu(pd) / 1e6
        print(f"{label:38s} {pc:8.3f} {rc:8.3f} {pc-rc:+8.3f} "
              f"{pe:8.1f} {re_:7.1f} {pe-re_:+6.1f} {lng:10.1f}")

    if read:
        print("\ncells read:")
        for p, r in read:
            print(f"  {p}  vs  {r}")


if __name__ == "__main__":
    main()

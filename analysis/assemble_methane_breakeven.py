#!/usr/bin/env python3
"""Break-even upstream-methane leak rates for every LNG pathway (A.10).

For each solved LNG cell: cumulative LNG imports over 2027-2050, the
implied methane throughput, the cell's combustion-CO2 advantage over a
matched non-LNG comparator, and the supply-chain leak rate at which that
advantage disappears on 100-year and 20-year warming potentials.

Conventions (report A.10): 19.3 kg CH4 per MMBtu; GWP100 = 30, GWP20 =
82.5 (IPCC AR6 WG1 Table 7.15, fossil-origin methane). Comparators are
matched on rooftop family, Waiau decision, and solar premium, so only the
fuel/plant decision differs.

  python3 analysis/assemble_methane_breakeven.py

Measured US rates for context (Sherwin et al. 2024, Nature 627:328-334):
production-weighted 2.95%; basins 0.75% (Appalachia) to 9.63% (NM Permian).
"""
import argparse
import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
YRS = {2027: 3, 2030: 5, 2035: 5, 2040: 5, 2045: 5, 2050: 5}
KG_CH4_PER_MMBTU = 19.3
GWP100, GWP20 = 30.0, 82.5

# (label, LNG cell, matched comparator)
OWN = [
    ("JERA 500 MW, bare-EPC", "nlv2b_wr_C6_LNG500_refbrent",
     "nlv2b_wr_C4_NOTHERMAL_refbrent"),
    ("JERA 500 MW, +20% capital", "nlv2b_wr_C6_LNG500_refbrent_j120",
     "nlv2b_wr_C4_NOTHERMAL_refbrent"),
    ("JERA 375 MW, bare-EPC", "nlv2b_C5_LNG375_refbrent",
     "nlv2b_C4_NOTHERMAL_refbrent"),
    ("JERA 375 MW, +20% capital", "nlv2b_C5_LNG375_refbrent_j120",
     "nlv2b_C4_NOTHERMAL_refbrent"),
    ("Conversion, optimized", "nlv2b_lngconv_opt_refbrent",
     "nlv2b_C4_NOTHERMAL_refbrent"),
    ("Conversion, no new plant", "nlv2b_lngconv_noplant_refbrent",
     "nlv2b_C4_NOTHERMAL_refbrent"),
    ("Conversion, HECO configuration", "nlv2b_lngconv_heco_refbrent",
     "nlv2b_C4_NOTHERMAL_refbrent"),
]
PLANS = [
    ("HSEO LNG vs its oil case, 1.2x", "nlv2s_plan_hseo_lng_refbrent",
     "nlv2s_plan_hseo_oil_refbrent"),
    ("HSEO LNG vs its oil case, 1.8x", "nlv2s_plan_hseo_lng_pv15_refbrent",
     "nlv2s_plan_hseo_oil_pv15_refbrent"),
    ("HSEO LNG vs its oil case, 2.04x", "nlv2s_plan_hseo_lng_pv17_refbrent",
     "nlv2s_plan_hseo_oil_pv17_refbrent"),
    ("HSEO LNG vs least-cost, 1.2x", "nlv2s_plan_hseo_lng_refbrent",
     "nlv2s_C4_NOTHERMAL_refbrent"),
    ("HSEO LNG vs least-cost, 1.8x", "nlv2s_plan_hseo_lng_pv15_refbrent",
     "nlv2s_be_pv15_C4_NOTHERMAL_refbrent"),
    ("HSEO LNG vs least-cost, 2.04x", "nlv2s_plan_hseo_lng_pv17_refbrent",
     "nlv2s_be_pv17_C4_NOTHERMAL_refbrent"),
]


def for_design(cell, design):
    """Insert the quota-revision tag ahead of the oil-path suffix.

    Only the plan cells carry a revision; the LNG-pathway rows in PATHWAYS are
    our own scenarios and are unaffected, which is why A.10's JERA-pathway
    table stayed valid when the plan tags were discarded.
    """
    if design == "floors" or "_plan_" not in cell:
        return cell
    return re.sub(r"_(refbrent|lowbrent|futbrent|highbrent)$",
                  rf"_{design}_\1", cell)


def best(cell):
    """Prefer the tightest available solve; STALE_ dirs are ignored."""
    for pre in ("R010_", "R0015_", ""):
        d = REPO / (pre + "outputs_" + cell)
        if (d / "total_cost.txt").exists():
            return d
    return None


def cum_co2_mt(d):
    return sum(float(r["DispatchEmissions_tCO2_per_typical_yr"] or 0)
               * YRS[int(r["period"])]
               for r in csv.DictReader(open(d / "dispatch_annual_summary.csv"))) / 1e6


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


def table(title, rows):
    print(f"\n== {title}")
    print(f"{'pathway':34s} {'imports':>9} {'CH4 Mt':>7} {'edge Mt':>8} "
          f"{'BE 100yr':>9} {'BE 20yr':>8}")
    for label, lng_cell, ref_cell in rows:
        ld, rd = best(lng_cell), best(ref_cell)
        if ld is None or rd is None:
            print(f"{label:34s}   [pending: "
                  f"{lng_cell if ld is None else ref_cell}]")
            continue
        imp = lng_mmbtu(ld)
        thr = imp * KG_CH4_PER_MMBTU / 1e9
        edge = cum_co2_mt(rd) - cum_co2_mt(ld)
        if thr <= 0:
            continue
        if edge <= 0:
            print(f"{label:34s} {imp/1e6:8.1f}M {thr:7.2f} {edge:+8.2f} "
                  f"{'—':>9} {'—':>8}   (no combustion edge to erase)")
            continue
        print(f"{label:34s} {imp/1e6:8.1f}M {thr:7.2f} {edge:+8.2f} "
              f"{edge/(thr*GWP100)*100:8.2f}% {edge/(thr*GWP20)*100:7.2f}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", choices=("hybrid", "firmfloor", "windband", "floors"),
                    default="firmfloor",
                    help="which plan-quota revision's cells to price; "
                         "'floors' reproduces the discarded floors-only tags")
    args = ap.parse_args()
    globals()["PLANS"] = [(lbl, for_design(a, args.design),
                           for_design(b, args.design)) for lbl, a, b in PLANS]
    print(f"plan cells: {args.design} revision")
    print("Break-even supply-chain methane leak rates (A.10 conventions: "
          f"{KG_CH4_PER_MMBTU} kg CH4/MMBtu, GWP100 {GWP100:.0f}, "
          f"GWP20 {GWP20:.1f})")
    table("Our LNG pathways vs matched no-new-thermal least cost "
          "(base rooftop, reference oil)", OWN)
    table("The HSEO LNG plan cell, by comparator and solar premium", PLANS)
    print("\nMeasured US supply chains (Sherwin et al. 2024): "
          "production-weighted 2.95%; basins 0.75%-9.63%.")


if __name__ == "__main__":
    main()

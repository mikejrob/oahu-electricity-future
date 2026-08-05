#!/usr/bin/env python3
"""Does a solved plan cell actually reproduce the plan's generation mix?

A price tag is only the plan's price if the cell that produced it runs the
plan's mix. The floors-only design failed exactly here: the cells met every
floor and then filled the unpinned third of the mix with cheap solar instead
of the plan's biofuel, reaching 2.1x the plan's utility solar in 2045-2050.
The tags were discarded on that finding, which was computed by hand and
survives only as a sentence in build_plan_quotas.py. This is that check, so
the next design change is judged against a number that can be re-run.

Plan levels are backed out of the quota file's floors rather than re-derived
from plan shares, because the floor is what the solve was actually held to,
and the two builders read different sources (HSEO from sources/plan_mix/,
IGP from the Supplemental tables via build_igp_plan_tables.py, while
igp_fig23_shares.csv calls the BASE scenario "preferred"). Reading the
enforced artifact avoids picking the wrong one.

Categories follow model/plan_mix_quota.py exactly, including the baseload
cogen carve-out and the --plan-quota-fossil-exempt plants.

    python3 analysis/audit_plan_mix_fidelity.py
    python3 analysis/audit_plan_mix_fidelity.py --cells outputs_nlv2s_plan_hseo_oil_refbrent
"""
import argparse
import csv
import glob
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# the multipliers the builders apply when writing floors
CLEAN_FLOOR = 0.98
FOSSIL_FLOOR = 0.95
# gen_is_baseload fossil units, outside the quota's constrained set
COGENS = ("Hawaii_Cogen", "Tesoro_Hawaii")
CAT_SOURCES = ("LSFO", "Diesel", "LNG", "multiple")
# how a cell's outputs_ name maps to the quota file it was solved against
QUOTA_FOR = {
    "nlv2a_plan_igp_pref": "plan_quota_igp_pref_nlv2a.csv",
    "nlv2a_plan_igp_alt_xf": "plan_quota_igp_alt_nlv2a_xf.csv",
    "nlv2b_plan_igp_alt": "plan_quota_igp_alt_nlv2b.csv",
    "nlv2b_plan_igp_pref_xf": "plan_quota_igp_pref_nlv2b_xf.csv",
    "nlv2s_plan_hseo_oil": "plan_quota_hseo_oil_nlv2s.csv",
    "nlv2s_plan_hseo_lng": "plan_quota_hseo_lng_nlv2s.csv",
}
EXEMPT_FOR = {"igp": ("Kalaeloa_CC",), "hseo": ()}


def quota_file(cell):
    """Longest matching prefix wins, so _xf beats its own base name."""
    stem = cell[len("outputs_"):]
    best = None
    for k, v in QUOTA_FOR.items():
        if stem.startswith(k) and (best is None or len(k) > len(best[0])):
            best = (k, v)
    return best[1] if best else None


def fuel_cell_gwh(cell):
    """Hydrogen fuel-cell generation, GWh/yr, weighted like the model does.

    dispatch_annual_summary has no fuel-cell row, so a firm quota looks
    unchecked unless this is added -- which is how the first HSEO firm-floor
    cell appeared to skip its firm row entirely.
    """
    fam = next((f for f in ("nlv2a", "nlv2b", "nlv2s") if f in cell), None)
    inp = REPO / f"inputs_{fam}"
    f = REPO / cell / "DispatchFuelCellMW.csv"
    if not fam or not f.exists() or not inp.exists():
        return {}
    plen = {int(r["INVESTMENT_PERIOD"]):
            float(r["period_end"]) - float(r["period_start"])
            for r in csv.DictReader(open(inp / "periods.csv"))}
    ts = {r["TIMESERIES"]: (int(r["ts_period"]), float(r["ts_duration_of_tp"]),
                            float(r["ts_scale_to_period"]))
          for r in csv.DictReader(open(inp / "timeseries.csv"))}
    tp = {r["timepoint_id"]: r["timeseries"]
          for r in csv.DictReader(open(inp / "timepoints.csv"))}
    out = {}
    for r in csv.DictReader(open(f)):
        v = float(r["DispatchFuelCellMW"] or 0)
        if v <= 0:
            continue
        per, dur, scale = ts[tp[r["DispatchFuelCellMW_index_2"]]]
        out[per] = out.get(per, 0.0) + v * dur * scale / plen[per] / 1000.0
    return out


def cell_mix(cell, exempt):
    """Annual GWh by quota category, per period, from the solved cell."""
    out = {}
    p = REPO / cell / "dispatch_annual_summary.csv"
    if not p.exists():
        return None
    for r in csv.DictReader(open(p)):
        per = int(r["period"])
        tech, src = r["gen_tech"], r["gen_energy_source"]
        name = r.get("generation_project", "") or tech
        e = float(r["Energy_GWh_typical_yr"] or 0)
        d = out.setdefault(per, {"usolar": 0.0, "offshore": 0.0,
                                 "wind": 0.0, "fossil": 0.0, "firm": 0.0})
        if "CentralTrackingPV" in tech:
            d["usolar"] += e
        if tech == "OffshoreWind":
            d["offshore"] += e
            d["wind"] += e
        elif tech == "OnshoreWind":
            d["wind"] += e
        if src in CAT_SOURCES and tech not in COGENS \
                and not any(x in tech or x in name for x in exempt):
            d["fossil"] += e
            d["firm"] += e          # firm = the fossil set plus fuel cells
    for per, gwh in fuel_cell_gwh(cell).items():
        if per in out:
            out[per]["firm"] += gwh
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", nargs="*", default=None)
    ap.add_argument("--design", choices=("hybrid", "firmfloor", "windband", "floors"),
                    default=None,
                    help="audit only cells of this revision. Each cell is "
                         "always judged against the quota file it was SOLVED "
                         "with, inferred from its directory name -- judging a "
                         "cell against a revision it never saw reports "
                         "violations that mean nothing")
    ap.add_argument("--tol", type=float, default=0.05,
                    help="flag a category off the plan by more than this")
    args = ap.parse_args()

    cells = args.cells or sorted(
        d[len(str(REPO)) + 1:] for d in glob.glob(str(REPO / "outputs_*plan_*")))
    worst = []
    for cell in cells:
        design = ("hybrid" if "_hybrid_" in cell
                                 else "firmfloor" if "_firmfloor_" in cell
                                 else "windband" if "_windband_" in cell
                                 else "floors")
        if args.design and design != args.design:
            continue
        qf = quota_file(cell)
        if qf and design in ("firmfloor", "hybrid"):
            qf = qf.replace("plan_quota_",
                            "plan_quota_ff_" if design == "firmfloor"
                            else "plan_quota_hy_")
        if not qf or not (REPO / cell / "dispatch_annual_summary.csv").exists():
            continue
        exempt = EXEMPT_FOR["igp" if "igp" in cell else "hseo"]
        mix = cell_mix(cell, exempt)
        floors = {}
        for r in csv.DictReader(open(REPO / "quotas" / qf)):
            if r["bound"] == "min":
                mult = FOSSIL_FLOOR if r["category"] == "fossil" else CLEAN_FLOOR
                floors[(int(r["period"]), r["category"])] = float(r["gwh"]) / mult

        print(f"\n=== {cell}  (vs {qf}) ===")
        print(f"  {'yr':<6}{'category':<10}{'plan':>10}{'cell':>10}{'ratio':>8}")
        for (per, cat), plan in sorted(floors.items()):
            got = mix.get(per, {}).get(cat)
            if got is None or plan <= 0:
                continue
            ratio = got / plan
            flag = "  <-- off plan" if abs(ratio - 1) > args.tol else ""
            print(f"  {per:<6}{cat:<10}{plan:>10,.0f}{got:>10,.0f}"
                  f"{ratio:>7.2f}x{flag}")
            if abs(ratio - 1) > args.tol:
                worst.append((abs(ratio - 1), cell, per, cat, ratio))

    if worst:
        worst.sort(reverse=True)
        print(f"\n{len(worst)} category-periods off the plan by more than "
              f"{args.tol:.0%}; largest:")
        for _, cell, per, cat, ratio in worst[:8]:
            print(f"  {ratio:5.2f}x  {per} {cat:<9} "
                  f"{cell[len('outputs_'):]}")
    else:
        print("\nevery category within tolerance of its plan level")


if __name__ == "__main__":
    main()

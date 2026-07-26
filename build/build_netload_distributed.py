#!/usr/bin/env python3
"""build_netload_distributed.py — exogenous distributed PV+storage net-load.

Refines the model's treatment of behind-the-meter distributed solar+storage.
The base inputs carry 674 MW of legacy rooftop PV as generators that age out to
zero by 2050 (max_age 30 on <=2020 vintages) and add nothing new — so the model
serves the full gross load from utility resources in the out-years and overbuilds
utility solar and land. Reality (FERC 714 / HECO DER records): 766 MW today,
growing, battery-paired since ~2020.

This script treats distributed PV+storage as an EXOGENOUS net-load reduction
(the convention in HECO's IGP, HSEO's model, and Matthias's heco_outlook module,
and what the author directed). It:
  1. removes the legacy DistPV generators (so no double count / no model-optimized
     distributed), and
  2. subtracts a fixed distributed generation profile from gross load -> net load.

Two capacity trajectories (author-approved):
  - base       : HECO/HSEO IGP DER forecast, ~flat (766 -> ~1,000 MW by 2050)
  - sensitivity: actual ~40 MW/yr trend with saturation taper (766 -> ~1,560 MW)

Two dispatch shapes, both data-anchored:
  - legacy PV-only (pre-2020, ~600 MW, minimal battery): SAM DistPV shape, midday.
  - new PV+battery (2020+, ~1 MWh/MW): the same PV energy shifted toward the
    evening (battery charges from midday surplus, discharges into the evening
    peak) -- the signature observed in the FERC 714 2020->2024 net-load change.

Usage: python build/build_netload_distributed.py {base|sensitivity} <out_inputs_dir>
Writes a modified copy of `inputs/` with net loads.csv and no DistPV builds.
"""
import csv, shutil, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# source inputs dir is overridable via the 3rd CLI arg (default: inputs)
SRC = REPO / (sys.argv[3] if len(sys.argv) > 3 else "inputs")

# --- distributed PV capacity (MW) by model period, Oahu ---
# anchored on 766 MW actual (2025, HECO DER records). Legacy (pre-2020) ~= 600 MW.
TRAJ = {
    "base":        {2027: 800, 2030: 850, 2035: 890, 2040: 930, 2045: 965, 2050: 1000},
    "sensitivity": {2027: 820, 2030: 960, 2035: 1140, 2040: 1300, 2045: 1440, 2050: 1560},
}
LEGACY_MW = 600.0   # pre-2020 rooftop, PV-only shape; the remainder is new PV+battery

# battery evening-shift for new capacity: move this fraction of midday (10-15h)
# output into the evening (18-22h), energy-conserving (matches the FERC signature).
SHIFT_FRAC = 0.40
MIDDAY = {10, 11, 12, 13, 14, 15}
EVENING = {18, 19, 20, 21, 22}


def load_hour_map():
    hr = {}
    for r in csv.DictReader(open(SRC / "timepoints.csv")):
        hr[r["timepoint_id"]] = int(r["timestamp"][11:13])
    return hr


def distpv_cf_by_hour():
    """SAM FlatDistPV mean CF by hour of day (the legacy PV-only shape)."""
    from collections import defaultdict
    acc = defaultdict(list)
    hr = load_hour_map()
    for r in csv.DictReader(open(SRC / "variable_capacity_factors.csv")):
        if "DistPV" in r["GENERATION_PROJECT"]:
            h = hr.get(r["timepoint"])
            if h is not None:
                acc[h].append(float(r["gen_max_capacity_factor"]))
    return {h: sum(v) / len(v) for h, v in acc.items()}


def new_shape(L):
    """PV+battery shape: shift SHIFT_FRAC of midday output into the evening,
    spread evenly across EVENING hours (energy-conserving)."""
    N = dict(L)
    shifted = sum(L.get(h, 0.0) * SHIFT_FRAC for h in MIDDAY)
    for h in MIDDAY:
        N[h] = L.get(h, 0.0) * (1 - SHIFT_FRAC)
    for h in EVENING:
        N[h] = N.get(h, 0.0) + shifted / len(EVENING)
    return N


def main(traj, outdir):
    outdir = Path(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    shutil.copytree(SRC, outdir)
    cap = TRAJ[traj]
    L = distpv_cf_by_hour()
    N = new_shape(L)
    hr = load_hour_map()

    # net load = gross - [legacy*L(h) + new(period)*N(h)]
    rows = list(csv.DictReader(open(SRC / "loads.csv")))
    tp_period = {r["timepoint_id"]: int(r["timestamp"][:4]) for r in
                 csv.DictReader(open(SRC / "timepoints.csv"))}
    out = []
    for r in rows:
        tp = r["TIMEPOINT"]; h = hr[tp]; per = tp_period[tp]
        new_mw = max(cap[per] - LEGACY_MW, 0.0)
        reduction = LEGACY_MW * L.get(h, 0.0) + new_mw * N.get(h, 0.0)
        gross = float(r["zone_demand_mw"])
        net = max(gross - reduction, 0.05 * gross)   # floor to avoid nonpositive
        out.append({"LOAD_ZONE": r["LOAD_ZONE"], "TIMEPOINT": tp,
                    "zone_demand_mw": f"{net:.6f}"})
    with open(outdir / "loads.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["LOAD_ZONE", "TIMEPOINT", "zone_demand_mw"])
        w.writeheader(); w.writerows(out)

    # Neutralize the in-model DistPV generators so distributed is counted ONLY on
    # the (netted) load side -- no double count. Keep every row/structure intact
    # (removing DistPV rows breaks Pyomo's CF Set indexing); just set the DistPV
    # capacity factor to 0 so the 674 MW predetermined DistPV generates nothing.
    # Its sunk predetermined capital is a constant across all scenarios, so it
    # cancels in every reported difference-vs-no-new-plant.
    vcf = list(csv.reader(open(SRC / "variable_capacity_factors.csv")))
    hdr = vcf[0]; cfi = hdr.index("gen_max_capacity_factor")
    for r in vcf[1:]:
        if "DistPV" in r[0]:
            r[cfi] = "0.0"
    with open(outdir / "variable_capacity_factors.csv", "w", newline="") as f:
        csv.writer(f).writerows(vcf)

    # report
    import statistics as st
    g = st.mean(float(r["zone_demand_mw"]) for r in rows)
    n = st.mean(float(r["zone_demand_mw"]) for r in out)
    print(f"[{traj}] wrote {outdir.name}: gross avg {g:.0f} MW -> net avg {n:.0f} MW "
          f"(distributed {cap[2027]}->{cap[2050]} MW); DistPV CF zeroed (netted on load side)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

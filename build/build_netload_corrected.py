#!/usr/bin/env python3
"""build_netload_corrected.py -- net-load from distributed PV+storage, SYNCHRONIZED
to site capacity factors and the firmed empirical estimates.

NAMING: this is the corrected distributed-solar treatment, release pre-v1.01 (the withdrawn working paper
as first circulated let rooftop PV retire to zero). It is NOT "v2"; v2 is the
regional/nodal grid model (see V2.md). Internal artifact prefixes "nlv2*" in
inputs_/outputs_/scenarios/ mean "net-load, revision 2 of the v1 distributed
treatment" and predate this note; they are frozen because solve fleets
reference them.

Synchronized to
the model's per-timepoint site capacity factors and calibrated to the firmed
empirical estimates (analysis/, radiation-identified from FERC 714 + NSRDB).

Improvements over build_netload_distributed.py (the first-fleet version):
  1. PER-TIMEPOINT CF, not an hour-of-day average -- distributed PV now moves
     with the SAME weather realization as utility-scale solar and demand, so a
     cloudy timepoint has low distributed AND low utility solar together (this
     governs curtailment and firm-capacity sizing). Zone-weighting was checked
     and is immaterial (install-weighted CF 0.1805 vs model 0.1822, <1%), so the
     model's existing DistPV CF is used.
  2. GRID-VISIBLE netting with the behind-the-meter wedge removed. The estimated
     grid-load reduction is beta ~= 0.76 x physical generation; the other ~24%
     serves induced demand (EVs charged from own solar) that is self-supplied and
     never crosses the meter. That demand is NOT in grid load and is not served,
     so only the grid-visible fraction is netted, and the existing fleet's wedge
     is removed from gross. For the EXISTING fleet this recovers ferc_net exactly
     (gross was built as ferc_net + full physical generation); for GROWTH only
     the grid-visible fraction nets.
        effective_PV_MW(period) = WEDGE*EXISTING_MW + (1-WEDGE)*installed_MW(period)
        PV_reduction(t) = effective_PV_MW * CF_DistPV(t)
  3. FIRMED battery: 0.454 MWh delivered to evening per installed MWh per day
     (radiation-identified, passes the physics cap 0.62), spread over 19-22h by
     the estimated weights; charged midday from own PV (reduces midday export).

Usage: python build/build_netload_corrected.py {base|sensitivity} <out_inputs_dir> [source_dir]
"""
import csv, shutil, sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / (sys.argv[3] if len(sys.argv) > 3 else "inputs")
ANA = REPO / "analysis"

# installed distributed PV (MW) by model period
TRAJ = {
    "base":        {2027: 800, 2030: 850, 2035: 890, 2040: 930, 2045: 965, 2050: 1000},
    "sensitivity": {2027: 820, 2030: 960, 2035: 1140, 2040: 1300, 2045: 1440, 2050: 1560},
    # accelerated = 2*sensitivity - base: ad-hoc "unleashed rooftop" projection for
    # unlimited sellback at avoided cost (see report policy discussion)
    "accel":       {2027: 840, 2030: 1070, 2035: 1390, 2040: 1670, 2045: 1915, 2050: 2120},
}
EXISTING_MW = 674.0          # in-model predetermined DistPV (2013-2020 vintages)
WEDGE = 0.24                 # g-beta induced-demand fraction (firmed, stable ~0.24)

# firmed battery (analysis/evening_shift_parameterization_firmed.csv)
BATT_DELIVER = 0.4538        # MWh delivered to evening per installed MWh per day
BATT_RTE = 0.86             # round-trip efficiency (charge = deliver / rte)
# firmed 19-22h weights (0.219/0.322/0.250/0.209) remapped to the model's
# even-hour (2-hourly) sampling by nearest sampled hour: 19,20->20h ; 21,22->22h.
DISCHARGE_W = {20: 0.5412, 22: 0.4588}   # sums to 1, all energy in the evening
CHARGE_HOURS = {10, 12, 14}              # sampled midday hours
# installed distributed battery energy (MWh): ~250 today (der records).
# New installs: ~1 MWh/MW on the base/sensitivity trajectories (observed program mix);
# 2 MWh/MW on the accelerated trajectory (all-TPO storage-heavy installs, e.g. a
# 6.5 kW system with one 13.5 kWh Powerwall ~= 2 MWh/MW; post-2027 only
# intermediary-owned batteries retain 48E credits, pushing exactly this config).
BATT_MWH_PER_NEW_MW = {"base": 1.0, "sensitivity": 1.0, "accel": 2.0}
def batt_mwh(pv_mw, traj):
    return 250.0 + max(pv_mw - 766.0, 0.0) * BATT_MWH_PER_NEW_MW[traj]


def tp_info():
    """timepoint_id -> (period_year, hour_of_day)"""
    info = {}
    for r in csv.DictReader(open(SRC / "timepoints.csv")):
        t = r["timepoint_id"]; ts = r["timestamp"]
        info[t] = (int(ts[:4]), int(ts[11:13]))
    return info


def distpv_cf_per_tp():
    """per-timepoint mean DistPV capacity factor (synchronized site CF)."""
    acc = defaultdict(list)
    for r in csv.DictReader(open(SRC / "variable_capacity_factors.csv")):
        if "DistPV" in r["GENERATION_PROJECT"]:
            acc[r["timepoint"]].append(float(r["gen_max_capacity_factor"]))
    return {t: sum(v) / len(v) for t, v in acc.items()}


def main(traj, outdir):
    outdir = Path(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    shutil.copytree(SRC, outdir)
    cap = TRAJ[traj]
    info = tp_info()
    cf = distpv_cf_per_tp()

    # mean midday CF per period, to normalize the battery charge draw
    midday_cf = defaultdict(list)
    for t, c in cf.items():
        per, h = info[t]
        if h in CHARGE_HOURS:
            midday_cf[per].append(c)
    midday_cf_sum = {p: sum(v) for p, v in midday_cf.items()}   # per period, for charge weights

    rows = list(csv.DictReader(open(SRC / "loads.csv")))
    out = []
    for r in rows:
        t = r["TIMEPOINT"]; per, h = info[t]; c = cf.get(t, 0.0)
        eff_pv = WEDGE * EXISTING_MW + (1 - WEDGE) * cap[per]     # grid-visible + wedge-removed existing
        pv_red = eff_pv * c
        mwh = batt_mwh(cap[per], traj)
        discharge = mwh * BATT_DELIVER * DISCHARGE_W.get(h, 0.0)  # MW into evening
        # midday charge from own PV: total daily charge energy spread over midday by CF
        charge = 0.0
        if h in CHARGE_HOURS and midday_cf_sum.get(per):
            charge = (mwh * BATT_DELIVER / BATT_RTE) * (c / midday_cf_sum[per])
        reduction = pv_red + discharge - charge
        gross = float(r["zone_demand_mw"])
        net = max(gross - reduction, 0.05 * gross)
        out.append({"LOAD_ZONE": r["LOAD_ZONE"], "TIMEPOINT": t,
                    "zone_demand_mw": f"{net:.6f}"})
    with open(outdir / "loads.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["LOAD_ZONE", "TIMEPOINT", "zone_demand_mw"])
        w.writeheader(); w.writerows(out)

    # neutralize in-model DistPV generators (netted on load side; keep rows/Set indexing)
    vcf = list(csv.reader(open(SRC / "variable_capacity_factors.csv")))
    hdr = vcf[0]; cfi = hdr.index("gen_max_capacity_factor")
    for row in vcf[1:]:
        if "DistPV" in row[0]:
            row[cfi] = "0.0"
    with open(outdir / "variable_capacity_factors.csv", "w", newline="") as f:
        csv.writer(f).writerows(vcf)

    import statistics as st
    g = st.mean(float(r["zone_demand_mw"]) for r in rows)
    n = st.mean(float(x["zone_demand_mw"]) for x in out)
    print(f"[{traj}] {outdir.name}: gross {g:.0f} -> net {n:.0f} MW avg; "
          f"PV {cap[2027]}->{cap[2050]} MW, batt {batt_mwh(cap[2027], traj):.0f}->{batt_mwh(cap[2050], traj):.0f} MWh; "
          f"grid-visible (wedge {WEDGE}), per-timepoint CF, battery {BATT_DELIVER} MWh/MWh over 19-22h")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

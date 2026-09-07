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
  3. FIRMED battery: 0.454 MWh delivered to evening per installed MWh on the
     AVERAGE day (radiation-identified, passes the physics cap 0.62), spread
     over 19-22h by the estimated weights; charged the same day from own
     midday PV at the estimated round-trip efficiency.

CORRECTED 2026-09-05 (energy accounting). The pre-correction version wrote
daily ENERGY quantities directly into the MW column of loads.csv without
dividing by the 2-hour timepoint duration (doubling delivered energy), and
normalized the daily charge draw over every midday timepoint in the PERIOD
rather than within each representative day (charging each day ~1/13th of its
draw). The committed pre-v1.031 nlv2* loads embodied batteries delivering
~2x the estimate while charging ~2/13ths of it. This version:
  - scales each day's delivery with that day's midday radiation relative to
    the weighted period mean (the A.11 identification: sunnier middays charge
    batteries fuller and lower that evening's grid load), so the WEIGHTED
    AVERAGE day delivers exactly BATT_DELIVER and a dark day delivers little;
  - caps any single day at the physical bound PHYS_CAP (0.62 MWh/MWh);
  - charges each day's delivery/RTE within THAT day's midday blocks, spread
    by that day's CF;
  - divides all block energies by TP_HRS when writing MW;
  - ASSERTS, per representative day, that written discharge energy equals
    the day's target and that charge*RTE equals discharge, and per period
    that the weighted mean delivery equals BATT_DELIVER.
Independent verification of any built directory: build/check_netload_energy.py.

Usage: python build/build_netload_corrected.py {base|sensitivity|accel} <out_inputs_dir> [source_dir]
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
BATT_DELIVER = 0.4538        # MWh delivered to evening per installed MWh, AVERAGE day
BATT_RTE = 0.86              # round-trip efficiency (charge = deliver / rte)
PHYS_CAP = 0.62              # physical daily bound, MWh per installed MWh (A.11)
TP_HRS = 2.0                 # model timepoint duration (hours); energy = MW x TP_HRS
# firmed 19-22h weights (0.219/0.322/0.250/0.209) remapped to the model's
# even-hour (2-hourly) sampling by nearest sampled hour: 19,20->20h ; 21,22->22h.
# These are ENERGY shares of the day's delivery across the two evening blocks.
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
    """timepoint_id -> (period_year, hour_of_day, day_id)"""
    info = {}
    for r in csv.DictReader(open(SRC / "timepoints.csv")):
        t = r["timepoint_id"]; ts = r["timestamp"]
        info[t] = (int(ts[:4]), int(ts[11:13]), ts[:10])
    return info


def assert_duration():
    """TP_HRS must equal the data's ts_duration_of_tp — a resolution change
    (e.g. 1-hour/8760 operations) would otherwise silently mis-scale every
    battery flow. The empirical hour sets (CHARGE_HOURS, DISCHARGE_W) are
    also tied to the current 2-hourly sampled grid; see
    docs/RESOLUTION_ASSUMPTIONS.md before changing resolution."""
    durs = {float(r["ts_duration_of_tp"])
            for r in csv.DictReader(open(SRC / "timeseries.csv"))}
    if durs != {TP_HRS}:
        raise ValueError(
            f"TP_HRS={TP_HRS} but the data's ts_duration_of_tp is {sorted(durs)}"
            " — this builder's constants and hour sets assume the 2-hourly"
            " grid; see docs/RESOLUTION_ASSUMPTIONS.md")


def day_weights():
    """(period, day_id) -> days per year this representative day carries."""
    ts_w = {r["TIMESERIES"]: float(r["ts_scale_to_period"])
            for r in csv.DictReader(open(SRC / "timeseries.csv"))}
    w = {}
    for r in csv.DictReader(open(SRC / "timepoints.csv")):
        ts = r["timestamp"]
        w[(int(ts[:4]), ts[:10])] = ts_w[r["timeseries"]]
    # ts_scale_to_period is days per PERIOD; divide by the period's own
    # length (3 yr for 2027, 5 yr after) so weights are days/YEAR — the
    # uniform /5 understated 2027 diagnostics by 40% (re-audit finding 6)
    tot = {}
    for (per, day), v in w.items():
        tot[per] = tot.get(per, 0.0) + v
    return {k: v / round(tot[k[0]] / 365.0) for k, v in w.items()}


def distpv_cf_per_tp():
    """per-timepoint mean DistPV capacity factor (synchronized site CF)."""
    acc = defaultdict(list)
    for r in csv.DictReader(open(SRC / "variable_capacity_factors.csv")):
        if "DistPV" in r["GENERATION_PROJECT"]:
            acc[r["timepoint"]].append(float(r["gen_max_capacity_factor"]))
    return {t: sum(v) / len(v) for t, v in acc.items()}


def battery_day_schedule(info, cf):
    """Per representative day: delivery per installed MWh (e_day) and the
    day's midday CF total (for spreading the charge within the day).

    e_day = BATT_DELIVER x (day's mean midday CF / weighted period mean),
    capped at PHYS_CAP. Weighted mean of e_day over each period equals
    BATT_DELIVER (asserted), unless the cap binds (reported)."""
    w = day_weights()
    mid_cf = defaultdict(list)                     # (per, day) -> midday CFs
    for t, (per, h, day) in info.items():
        if h in CHARGE_HOURS:
            mid_cf[(per, day)].append(cf.get(t, 0.0))
    m_day = {k: sum(v) / len(v) for k, v in mid_cf.items()}
    mid_sum = {k: sum(v) for k, v in mid_cf.items()}

    e_day, capped = {}, []
    for per in sorted({k[0] for k in m_day}):
        keys = [k for k in m_day if k[0] == per]
        W = sum(w[k] for k in keys)
        M = sum(w[k] * m_day[k] for k in keys) / W
        for k in keys:
            e = BATT_DELIVER * m_day[k] / M
            if e > PHYS_CAP:
                capped.append(k)
                e = PHYS_CAP
            e_day[k] = e
        mean = sum(w[k] * e_day[k] for k in keys) / W
        assert abs(mean - BATT_DELIVER) <= 0.01 * BATT_DELIVER, (
            f"period {per}: weighted mean delivery {mean:.4f} != {BATT_DELIVER}")
    if capped:
        print(f"  note: PHYS_CAP {PHYS_CAP} binds on {len(capped)} day(s): "
              + ", ".join(f"{k[0]}/{k[1]}" for k in sorted(capped)))
    return e_day, mid_sum, w


def main(traj, outdir):
    outdir = Path(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    shutil.copytree(SRC, outdir)
    assert_duration()
    cap = TRAJ[traj]
    info = tp_info()
    cf = distpv_cf_per_tp()
    e_day, mid_sum, day_w = battery_day_schedule(info, cf)

    rows = list(csv.DictReader(open(SRC / "loads.csv")))
    out = []
    disch_e = defaultdict(float)                  # (per, day) -> MWh written
    charge_e = defaultdict(float)
    for r in rows:
        t = r["TIMEPOINT"]; per, h, day = info[t]; c = cf.get(t, 0.0)
        k = (per, day)
        eff_pv = WEDGE * EXISTING_MW + (1 - WEDGE) * cap[per]     # grid-visible + wedge-removed existing
        pv_red = eff_pv * c
        mwh = batt_mwh(cap[per], traj)
        e = mwh * e_day.get(k, 0.0)               # the day's delivered MWh
        # evening delivery: the day's energy, split by the estimated shares,
        # written as average MW over the 2-hour block
        discharge = e * DISCHARGE_W.get(h, 0.0) / TP_HRS
        # midday charge from own PV: the day's delivery/RTE, spread within
        # THIS day's midday blocks by CF, written as average MW
        charge = 0.0
        if h in CHARGE_HOURS and mid_sum.get(k):
            charge = (e / BATT_RTE) * (c / mid_sum[k]) / TP_HRS
        disch_e[k] += discharge * TP_HRS
        charge_e[k] += charge * TP_HRS
        reduction = pv_red + discharge - charge
        gross = float(r["zone_demand_mw"])
        net = max(gross - reduction, 0.05 * gross)
        out.append({"LOAD_ZONE": r["LOAD_ZONE"], "TIMEPOINT": t,
                    "zone_demand_mw": f"{net:.6f}"})

    # -------- conservation assertions: per representative day, the energy
    # actually written must equal the day's target, and charge*RTE = discharge
    for k, e in disch_e.items():
        per = k[0]
        target = batt_mwh(cap[per], traj) * e_day.get(k, 0.0)
        assert abs(e - target) < 1e-6 * max(target, 1.0), (k, e, target)
        assert abs(charge_e[k] * BATT_RTE - e) < 1e-6 * max(e, 1.0), (
            f"day {k}: charge {charge_e[k]:.3f} x RTE != discharge {e:.3f}")

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
    ann_d = sum(day_w[k] * e for k, e in disch_e.items()) / len({k[0] for k in disch_e})
    ann_c = sum(day_w[k] * e for k, e in charge_e.items()) / len({k[0] for k in charge_e})
    print(f"[{traj}] {outdir.name}: gross {g:.0f} -> net {n:.0f} MW avg; "
          f"PV {cap[2027]}->{cap[2050]} MW, batt {batt_mwh(cap[2027], traj):.0f}->{batt_mwh(cap[2050], traj):.0f} MWh; "
          f"battery {BATT_DELIVER} MWh/MWh avg day over 19-22h, day-CF-scaled; "
          f"mean-period discharge {ann_d/1000:.1f} / charge {ann_c/1000:.1f} GWh/yr "
          f"(ratio {ann_d/ann_c if ann_c else 0:.3f} = RTE {BATT_RTE})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

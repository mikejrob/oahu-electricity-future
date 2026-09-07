#!/usr/bin/env python3
"""check_netload_energy.py -- physical verification of a netted-load inputs dir.

Reconstructs the implied distributed-battery flows in <built_dir>/loads.csv
by subtracting the PV netting term from (gross - net), then checks PHYSICS,
not the builder's equations:

  1. CONSERVATION  per representative day: charge x RTE == discharge
     (a battery must draw more energy than it delivers).
  2. CAP           no day delivers more than PHYS_CAP (0.62 MWh) per
     installed MWh.
  3. CALIBRATION   the day-weighted average delivery equals BATT_DELIVER
     (0.4538 MWh per installed MWh) within 1 percent.
  4. PLACEMENT     discharge only in the evening blocks, charge only in the
     midday blocks; all other blocks carry a pure PV term.
  5. DistPV capacity factors are zeroed in the built dir (netted on load side).

Rows where the 5-percent-of-gross floor binds are excluded from the
decomposition and counted. Exit 0 = pass, 1 = fail.

This would have failed loudly on every pre-2026-09-05 nlv2* build (the
committed loads delivered ~2x BATT_DELIVER daily while charging ~2/13ths
of the draw -- see CORRECTIONS.md).

Usage: python build/check_netload_energy.py <traj> <built_dir> [source_dir]
       e.g. python build/check_netload_energy.py base inputs_nlv2b inputs
"""
import csv, sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))
import build_netload_corrected as B   # constants only; equations NOT reused

EVENING = set(B.DISCHARGE_W)
TOL_REL = 0.01


def run(traj, built, src):
    fail = []
    info = {}
    ts_w = {r["TIMESERIES"]: float(r["ts_scale_to_period"])
            for r in csv.DictReader(open(src / "timeseries.csv"))}
    day_w = {}
    for r in csv.DictReader(open(src / "timepoints.csv")):
        t, ts = r["timepoint_id"], r["timestamp"]
        info[t] = (int(ts[:4]), int(ts[11:13]), ts[:10])
        day_w[(int(ts[:4]), ts[:10])] = ts_w[r["timeseries"]]
    tot = {}
    for (per, day), v in day_w.items():
        tot[per] = tot.get(per, 0.0) + v
    day_w = {k: v / round(tot[k[0]] / 365.0) for k, v in day_w.items()}

    # independent duration check: the checker must NOT inherit a wrong
    # TP_HRS from the builder (a shared wrong constant would cancel in the
    # calibration test and pass) — read the data's own value and fail loud
    durs = {float(r["ts_duration_of_tp"])
            for r in csv.DictReader(open(src / "timeseries.csv"))}
    if durs != {B.TP_HRS}:
        fail.append(f"DURATION: builder TP_HRS={B.TP_HRS} but data "
                    f"ts_duration_of_tp={sorted(durs)} — every energy in "
                    "this check would be mis-scaled")

    cf = defaultdict(list)
    for r in csv.DictReader(open(src / "variable_capacity_factors.csv")):
        if "DistPV" in r["GENERATION_PROJECT"]:
            cf[r["timepoint"]].append(float(r["gen_max_capacity_factor"]))
    cf = {t: sum(v) / len(v) for t, v in cf.items()}

    gross = {r["TIMEPOINT"]: float(r["zone_demand_mw"])
             for r in csv.DictReader(open(src / "loads.csv"))}
    net = {r["TIMEPOINT"]: float(r["zone_demand_mw"])
           for r in csv.DictReader(open(built / "loads.csv"))}

    cap = B.TRAJ[traj]
    disch = defaultdict(float); charge = defaultdict(float)
    floored, stray = [], []
    for t, g in gross.items():
        per, h, day = info[t]; k = (per, day)
        if abs(net[t] - 0.05 * g) < 1e-4:                      # floor bound
            floored.append(t); continue
        eff_pv = B.WEDGE * B.EXISTING_MW + (1 - B.WEDGE) * cap[per]
        batt = (g - net[t]) - eff_pv * cf.get(t, 0.0)          # implied MW
        e = batt * B.TP_HRS                                    # implied MWh
        if h in EVENING and e > 1e-6:
            disch[k] += e
        elif h in B.CHARGE_HOURS and e < -1e-6:
            charge[k] += -e
        elif abs(e) > 1e-3:
            stray.append((t, h, e))

    if stray:
        fail.append(f"PLACEMENT: {len(stray)} blocks with battery-like flow "
                    f"outside evening/midday, e.g. {stray[:3]}")

    # per-day conservation and cap
    worst_ratio, bad_days = None, 0
    for k in sorted(set(disch) | set(charge)):
        d, c = disch.get(k, 0.0), charge.get(k, 0.0)
        mwh = B.batt_mwh(cap[k[0]], traj)
        if d / mwh > B.PHYS_CAP * (1 + TOL_REL):
            fail.append(f"CAP: day {k} delivers {d/mwh:.3f} MWh/MWh > {B.PHYS_CAP}")
        if d < 1e-6 and c < 1e-6:
            continue
        ratio = (c * B.BATT_RTE / d) if d > 1e-9 else float("inf")
        if abs(ratio - 1.0) > TOL_REL:
            bad_days += 1
            if worst_ratio is None or abs(ratio - 1) > abs(worst_ratio - 1):
                worst_ratio, worst_k, wd, wc = ratio, k, d, c
    if bad_days:
        fail.append(f"CONSERVATION: {bad_days} day(s) violate charge x RTE == "
                    f"discharge; worst {worst_k}: discharge {wd:.1f} MWh vs "
                    f"charge {wc:.1f} MWh (x RTE = {wc*B.BATT_RTE:.1f}; "
                    f"ratio {worst_ratio:.3f}, want 1.0)")

    # calibration: weighted average delivery per installed MWh
    for per in sorted({k[0] for k in day_w}):
        keys = [k for k in day_w if k[0] == per]
        W = sum(day_w[k] for k in keys)
        mean = sum(day_w[k] * disch.get(k, 0.0) for k in keys) / W \
            / B.batt_mwh(cap[per], traj)
        if abs(mean - B.BATT_DELIVER) > TOL_REL * B.BATT_DELIVER:
            fail.append(f"CALIBRATION {per}: weighted mean delivery "
                        f"{mean:.4f} MWh/MWh, want {B.BATT_DELIVER}")

    # DistPV neutralized in built dir
    live = sum(1 for r in csv.DictReader(open(built / "variable_capacity_factors.csv"))
               if "DistPV" in r["GENERATION_PROJECT"]
               and float(r["gen_max_capacity_factor"]) != 0.0)
    if live:
        fail.append(f"DISTPV: {live} non-zero DistPV capacity factors in built dir")

    ann_d = {p: sum(day_w[k] * disch.get(k, 0.0) for k in day_w if k[0] == p)
             for p in sorted({k[0] for k in day_w})}
    ann_c = {p: sum(day_w[k] * charge.get(k, 0.0) for k in day_w if k[0] == p)
             for p in sorted({k[0] for k in day_w})}
    print(f"== {built.name} (traj {traj}; source {src.name}) ==")
    print(f"   floored rows excluded: {len(floored)}")
    for p in ann_d:
        print(f"   {p}: discharge {ann_d[p]/1000:8.2f} GWh/yr   "
              f"charge {ann_c[p]/1000:8.2f} GWh/yr   "
              f"net {'+' if ann_d[p]>ann_c[p] else ''}{(ann_d[p]-ann_c[p])/1000:.2f}")
    if fail:
        print("FAIL:")
        for f_ in fail:
            print(f"   {f_}")
        return 1
    print("PASS: daily conservation, physics cap, calibration, placement, DistPV zeroed")
    return 0


if __name__ == "__main__":
    traj = sys.argv[1]
    built = Path(sys.argv[2])
    src = Path(sys.argv[3]) if len(sys.argv) > 3 else REPO / "inputs"
    sys.exit(run(traj, built, src))

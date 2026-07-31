#!/usr/bin/env python3
"""Build inputs for the pinned-schedule experiment (B minus A).

Question: what is optimal scheduling of the distributed battery fleet worth,
holding everything else fixed? The cross-representation comparison (dg* vs
nlv2*) cannot answer it — the representations differ in capital accounting
and profile conventions worth more than the scheduling signal at scale.

The dispatched (gross-load) inputs already predetermine the entire
distributed fleet — DistPV *and* DistBattery vintages — so the existing
solves are the free-schedule arm:

  A (existing R010_outputs_dg?_C4_NOTHERMAL_refbrent): fleet predetermined,
      schedule free — the optimizer dispatches the rooftop batteries.
  B  (outputs_dg?_ps_*): identical inputs plus model/pin_dist_battery.py,
      which pins the fleet to today's estimated behavior — charge from
      midday output, discharge spread evenly across the evening blocks,
      sized to deliver SHIFT_FRAC (40%, per build_netload_distributed.py)
      of the post-legacy fleet's midday output into the evening, capped by
      the predetermined fleet's energy capacity and ratings, cycling daily.

  B − A = the value of optimal scheduling, clean: identical capital,
  identical load, identical yield on both sides of the difference.

Writes inputs_dg{b,s,a}_pin/ (copy of inputs_dg{b,s,a}/ plus
dist_battery_schedule.csv; nothing else changes).

Run from the repository root:  python3 build/build_pinned_dist_inputs.py
"""
import csv
import shutil
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# operating rooftop trajectory (MW) per family — must match
# build_netload_distributed.py
TRAJ = {
    "dgb": {2027: 800, 2030: 850, 2035: 890, 2040: 930, 2045: 965, 2050: 1000},
    "dgs": {2027: 820, 2030: 960, 2035: 1140, 2040: 1300, 2045: 1440, 2050: 1560},
    "dga": {2027: 840, 2030: 1070, 2035: 1390, 2040: 1670, 2045: 1915, 2050: 2120},
}
LEGACY_MW = 600.0    # pre-2020 PV-only stock (no battery), as in the netted build
SHIFT_FRAC = 0.40    # fraction of new-fleet midday output delivered to evening
MAX_AGE = 15         # DistBattery gen_max_age (gen_info.csv)
CHARGE_EFF = 0.9     # gen_storage_efficiency (gen_info.csv)
MIDDAY = {10, 12, 14}    # 2-hour block start hours
EVENING = {18, 20, 22}
GEN = "Oahu_DistBattery"


def fleet_by_period(src, periods):
    """Predetermined DistBattery (MW, MWh) operating at each period start."""
    vintages = []
    for r in csv.DictReader(open(src / "gen_build_predetermined.csv")):
        if r["GENERATION_PROJECT"] == GEN:
            vintages.append((int(r["build_year"]),
                             float(r["build_gen_predetermined"]),
                             float(r["build_gen_energy_predetermined"])))
    out = {}
    for p in periods:
        mw = sum(v[1] for v in vintages if v[0] <= p < v[0] + MAX_AGE)
        mwh = sum(v[2] for v in vintages if v[0] <= p < v[0] + MAX_AGE)
        out[p] = (mw, mwh)
    return out


def main():
    for fam in ("dgb", "dgs", "dga"):
        src = REPO / f"inputs_{fam}"
        dst = REPO / f"inputs_{fam}_pin"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        ts_of, per_of, day_of, hour_of = {}, {}, {}, {}
        for r in csv.DictReader(open(src / "timepoints.csv")):
            t = r["timepoint_id"]
            ts_of[t] = r["timestamp"]
            per_of[t] = int(r["timestamp"][:4])
            day_of[t] = r["timestamp"][:10]
            hour_of[t] = int(r["timestamp"][11:13])
        periods = sorted(set(per_of.values()))
        fleet = fleet_by_period(src, periods)

        # mean DistPV capacity factor per timepoint (all DistPV projects, as
        # in build_netload_distributed.distpv_cf_by_hour)
        acc = defaultdict(list)
        for r in csv.DictReader(open(src / "variable_capacity_factors.csv")):
            if "DistPV" in r["GENERATION_PROJECT"]:
                acc[r["timepoint"]].append(float(r["gen_max_capacity_factor"]))
        cf = {t: sum(v) / len(v) for t, v in acc.items()}

        days = defaultdict(list)
        for t in ts_of:
            days[day_of[t]].append(t)
        sched = {}
        for day, tps in days.items():
            p = per_of[tps[0]]
            new_mw = TRAJ[fam].get(p, TRAJ[fam][max(TRAJ[fam])]) - LEGACY_MW
            mw_cap, e_cap = fleet[p]
            midday_tps = sorted(t for t in tps if hour_of[t] in MIDDAY)
            evening_tps = sorted(t for t in tps if hour_of[t] in EVENING)
            midday_out = sum(cf.get(t, 0.0) * new_mw * 2.0 for t in midday_tps)
            # stored energy per day: the target evening delivery, capped by
            # the fleet's energy capacity and by its power rating on both
            # the charge (stored/eff over 6 h) and discharge (over 6 h) side
            stored = min(SHIFT_FRAC * midday_out, e_cap,
                         mw_cap * 2.0 * len(midday_tps) * CHARGE_EFF,
                         mw_cap * 2.0 * len(evening_tps))
            for t in tps:
                if t in midday_tps and stored > 0:
                    sched[t] = ((stored / CHARGE_EFF) / (2.0 * len(midday_tps)),
                                0.0)
                elif t in evening_tps and stored > 0:
                    sched[t] = (0.0, stored / (2.0 * len(evening_tps)))
                else:
                    sched[t] = (0.0, 0.0)

        with open(dst / "dist_battery_schedule.csv", "w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["timepoint_id", "charge_mw", "discharge_mw"])
            for t in sorted(sched, key=lambda t: ts_of[t]):
                c, d = sched[t]
                w.writerow([t, round(c, 6), round(d, 6)])

        worst_c = max(c for c, _ in sched.values())
        worst_d = max(d for _, d in sched.values())
        print(f"{fam}: inputs_{fam}_pin written; max charge {worst_c:.0f} MW, "
              f"max discharge {worst_d:.0f} MW; fleet "
              + ", ".join(f"{p}:{fleet[p][0]:.0f}MW/{fleet[p][1]:.0f}MWh"
                          for p in periods))


if __name__ == "__main__":
    main()

"""Pin the distributed battery (Oahu_DistBattery) to a fixed daily schedule.

Today's observed behavior — charge from midday rooftop output, discharge into
the evening — is precomputed per timepoint by
build/build_pinned_dist_inputs.py and read from
<inputs>/dist_battery_schedule.csv (columns: timepoint_id, charge_mw,
discharge_mw).

Used by the pinned-schedule experiment: the B runs include this module; the
A' runs use the same inputs (same predetermined battery fleet) without it.
B minus A' isolates the value of optimal scheduling of the distributed fleet
with every accounting convention (capital, load basis, wedge, yield) held
identical on both sides.
"""
import csv
import os

from pyomo.environ import Constraint

GEN = "Oahu_DistBattery"
_cache = {}


def _schedule(m):
    path = os.path.join(m.options.inputs_dir, "dist_battery_schedule.csv")
    if path not in _cache:
        sched = {}
        with open(path) as f:
            for r in csv.DictReader(f):
                sched[str(r["timepoint_id"])] = (
                    float(r["charge_mw"]), float(r["discharge_mw"]))
        _cache[path] = sched
    return _cache[path]


def define_components(m):
    def charge_rule(m, t):
        if (GEN, t) not in m.STORAGE_GEN_TPS:
            return Constraint.Skip
        return m.ChargeStorage[GEN, t] == _schedule(m)[str(t)][0]

    m.Pin_DistBatt_Charge = Constraint(m.TIMEPOINTS, rule=charge_rule)

    def discharge_rule(m, t):
        if (GEN, t) not in m.GEN_TPS:
            return Constraint.Skip
        return m.DispatchGen[GEN, t] == _schedule(m)[str(t)][1]

    m.Pin_DistBatt_Discharge = Constraint(m.TIMEPOINTS, rule=discharge_rule)
    print("Oahu_DistBattery pinned to fixed daily schedule "
          "(dist_battery_schedule.csv).")

#!/usr/bin/env python3
"""build_distpv_generation.py -- distributed PV+storage as EXOGENOUS, growing,
DISPATCHING generation (Matthias Fripp / heco_outlook convention).

Contrast with build_netload_distributed.py, which subtracted distributed output
from load (demand side) and zeroed the DistPV generators. That is the wrong side
of the ledger: the v1 model's loads.csv is GROSS system load (avg 966 MW), and
DistPV is represented as predetermined generators that DISPATCH to serve it
(midday ~432 MW in 2027). The only defect is that the existing fleet (2013-2020
vintages, max_age 30) RETIRES to zero by 2050 with no replacement, so out-year
gross load loses its distributed offset and utility solar overbuilds.

This script fixes it in-framework, the way Matthias's model and the v1 baseline
both do: it EXTENDS the predetermined DistPV and DistBattery builds with new
vintages through 2050 so the distributed fleet does not age off the grid and
grows on the chosen trajectory. loads.csv stays GROSS and untouched. The
optimizer dispatches the added PV (curtailable in midday oversupply) and the
added batteries (charge midday, discharge evening) endogenously -- no hand-coded
shift, no forced must-take. This is the "generators dispatch optimally" version;
comparing its land/utility-solar build to the net-load version shows how much the
representation matters (curtailment + optimal storage vs a fixed load cut).

New capacity is sized to track the trajectory NET OF RETIREMENT: for each model
period, new_cumulative = target - surviving_existing. New PV is allocated across
the existing DistPV projects in proportion to their capacity (preserving the
Flat/Sloped capacity-factor mix). Paired DistBattery is added on the existing
Oahu_DistBattery project.

Capital costs are LEFT AS-IS (not zeroed): DistPV/DistBattery are endogenous
build candidates, so zeroing their cost would let the model build unlimited free
rooftop. Real costs are safe (the model will not build DistPV on its own -- it is
pricier per MW than utility solar) and correct as a resource-cost view. Because
the distributed trajectory is identical across every scenario in a run, its
capital cancels exactly in any difference-vs-baseline (the report's basis).

Usage: python build/build_distpv_generation.py {base|sensitivity} <out_inputs_dir> [source_dir]
"""
import csv, shutil, sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / (sys.argv[3] if len(sys.argv) > 3 else "inputs")

# distributed PV capacity target (MW installed, net of retirements) by period.
# base = HECO/HSEO IGP DER forecast (~flat); sensitivity = recent ~40 MW/yr trend.
TRAJ = {
    "base":        {2027: 800, 2030: 850, 2035: 890, 2040: 930, 2045: 965, 2050: 1000},
    "sensitivity": {2027: 820, 2030: 960, 2035: 1140, 2040: 1300, 2045: 1440, 2050: 1560},
    # accelerated = 2*sensitivity - base ("unleashed rooftop": unlimited sellback at
    # avoided cost). New installs pair 2 MWh/MW (6.5 kW + one 13.5 kWh Powerwall).
    "accel":       {2027: 840, 2030: 1070, 2035: 1390, 2040: 1670, 2045: 1915, 2050: 2120},
}
PERIODS = [2027, 2030, 2035, 2040, 2045, 2050]
DISTPV_MAX_AGE = 30

# --- distributed battery pairing for NEW capacity (dispatched by the optimizer) ---
# recent Oahu installs (post Battery Bonus) pair storage with most new rooftop PV.
# These are assumptions to confirm; the optimizer dispatches within them.
# battery pairing on NEW capacity, per trajectory (empirically grounded):
# base/sensitivity ~1 MWh/MW (observed program mix, ~50% attach at ~2 MWh/MW);
# accel 2 MWh/MW (all-TPO storage-heavy: 6.5 kW + one Powerwall; 48E post-2027).
BATT_MWH_PER_MW = {"base": 1.0, "sensitivity": 1.0, "accel": 2.0}
BATT_HOURS      = 3.0    # duration -> power (MW) = energy (MWh) / hours
BATT_PROJECT    = "Oahu_DistBattery"


def existing_distpv():
    """existing DistPV predetermined capacity: by vintage year and by project."""
    by_year = defaultdict(float)
    by_proj = defaultdict(float)
    for r in csv.DictReader(open(SRC / "gen_build_predetermined.csv")):
        row = list(r.values())
        g, by, mw = row[0], int(row[1]), float(row[2])
        if "DistPV" in g:
            by_year[by] += mw
            by_proj[g] += mw
    return by_year, by_proj


def surviving(by_year, period):
    return sum(mw for y, mw in by_year.items() if period < y + DISTPV_MAX_AGE)


def main(traj, outdir):
    outdir = Path(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    shutil.copytree(SRC, outdir)

    tgt = TRAJ[traj]
    by_year, by_proj = existing_distpv()
    proj_total = sum(by_proj.values())
    shares = {g: c / proj_total for g, c in by_proj.items()}

    # cumulative new PV needed at each period = target - surviving existing
    new_cum = {p: max(tgt[p] - surviving(by_year, p), 0.0) for p in PERIODS}
    # incremental new build per period (new vintages >=2027 do not retire in-horizon)
    new_bld = {}
    prev = 0.0
    for p in PERIODS:
        new_bld[p] = max(new_cum[p] - prev, 0.0)
        prev = new_cum[p]

    # --- append predetermined builds ---
    pre_rows = list(csv.reader(open(SRC / "gen_build_predetermined.csv")))
    hdr = pre_rows[0]
    add = []
    for p in PERIODS:
        pv = new_bld[p]
        if pv <= 0:
            continue
        # allocate this period's new PV across existing DistPV projects by share
        for g, sh in shares.items():
            mw = pv * sh
            if mw <= 1e-9:
                continue
            add.append([g, p, f"{mw:.6f}", "."])   # PV: no energy column
        # paired distributed battery on the existing DistBattery project
        be = pv * BATT_MWH_PER_MW[traj]
        bp = be / BATT_HOURS
        if bp > 1e-9:
            add.append([BATT_PROJECT, p, f"{bp:.6f}", f"{be:.6f}"])
    with open(outdir / "gen_build_predetermined.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerows(pre_rows)
        w.writerows(add)

    # sanity: report installed trajectory (existing surviving + new cumulative)
    print(f"[{traj}] wrote {outdir.name}")
    print(f"  {'period':>6} {'surv_exist':>10} {'new_cum':>8} {'installed':>9} {'target':>7} "
          f"{'new_batt_MW':>11}")
    bcum = 0.0
    for p in PERIODS:
        s = surviving(by_year, p)
        bcum += new_bld[p] * BATT_MWH_PER_MW[traj] / BATT_HOURS
        print(f"  {p:>6} {s:>10.0f} {new_cum[p]:>8.0f} {s+new_cum[p]:>9.0f} {tgt[p]:>7} "
              f"{bcum:>11.0f}")
    print(f"  battery pairing: {BATT_MWH_PER_MW[traj]:.1f} MWh/MW_PV ({BATT_HOURS:.0f}h duration); "
          f"loads.csv left GROSS; DistPV/DistBattery dispatched by the optimizer")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

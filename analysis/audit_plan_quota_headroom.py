#!/usr/bin/env python3
"""Is a plan's rescaled mix reachable on our grid, and does the RPS bind?

Two candidate explanations for an infeasible pinned-mix cell, both settled
here without solving anything.

 1. RPS. Does the quota force more fossil than the RPS allows? The test is the
    fossil FLOOR, not the ceiling -- a ceiling is permissive, the model may
    always burn less. Add the refinery cogens, which burn fossil but sit
    outside the constrained set (gen_is_baseload, so they cannot respond to a
    quota) and still count against the RPS. If floor + cogens exceeds the
    non-renewable share the target permits, quota and RPS contradict and no
    solve exists.

 2. Energy balance. The quota pins fossil, utility solar and offshore and
    leaves the plan's other categories to the optimizer. Two of them our grid
    cannot match: onshore wind is capped at 150 MW by the county setback
    against plan shares near 10%, and refuse is capped at H-POWER's 86 MW.
    Their shortfall has to come from a pinned category -- so in a period where
    every pinned ceiling binds at once, the ceilings plus the physical caps
    can sum to less generation than serving load requires. That is a shortfall
    no amount of building fixes.

RPS is measured against total generation, not load (switch_model.hawaii.rps:
RPSEligiblePower >= target * RPSTotalPower). Generation exceeds served load by
transmission losses, storage round-trip and electrolysis draw, so the required
generation is taken from the family's own solved cell rather than assumed.

    python3 analysis/audit_plan_quota_headroom.py
    python3 analysis/audit_plan_quota_headroom.py --plan hseo_oil
"""
import argparse
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PERIODS = [2030, 2035, 2040, 2045, 2050]

# gen_is_baseload fossil units: exempt from the quota's constrained set, still
# non-renewable in the RPS accounting
COGENS = ("Hawaii_Cogen", "Tesoro_Hawaii")
# RPS-eligible generation: NON_FUEL_ENERGY_SOURCES less Battery, plus the
# rps_eligible fuels (Biodiesel, Pellet-Biomass) burned in multi-fuel units
RENEWABLE_TECH = ("CentralTrackingPV", "OffshoreWind", "OnshoreWind", "EGS",
                  "H-Power", "FlatDistPV", "SlopedDistPV")
# categories our grid cannot expand to the plan's share, with the binding limit
HARD_CAPPED = {"onshore": "OnshoreWind (150 MW county setback)",
               "refuse": "H-POWER (86 MW)"}

PLANS = {"hseo_oil": ("sources/plan_mix/hseo_oil.csv", "nlv2s"),
         "hseo_lng": ("sources/plan_mix/hseo_lng.csv", "nlv2s")}


def plan_grid_shares(path):
    """Category shares of the plan's GRID supply (customer solar removed)."""
    out = {}
    rd = csv.reader(open(REPO / path))
    hdr = [h.strip() for h in next(rd)]
    for row in rd:
        y = int(row[0])
        if y not in PERIODS:
            continue
        v = {hdr[i]: float(row[i]) for i in range(1, len(hdr)) if row[i]}
        dist = v.get("Solar - Distributed", 0)
        grid = sum(v.values()) - dist
        usolar = v.get("Solar  - Utility Grid", 0) or v.get("Solar - Utility Grid", 0)
        out[y] = {"fossil": (v.get("Oil", 0) + v.get("LNG", 0)) / grid,
                  "usolar": usolar / grid,
                  "onshore": v.get("Onshore Wind", 0) / grid,
                  "offshore": v.get("Offshore Wind", 0) / grid,
                  "refuse": v.get("Refuse", 0) / grid}
    return out


def solved(family, plan):
    """served load, total generation, and per-category energy from the cell."""
    d = REPO / f"outputs_{family}_plan_{plan}_refbrent"
    served = {int(r["PERIOD"]): float(r["SystemDemandPerYear_MWh"]) / 1e3
              for r in csv.DictReader(open(d / "electricity_cost.csv"))}
    gen, cat = {}, {}
    for r in csv.DictReader(open(d / "dispatch_annual_summary.csv")):
        p, tech = int(r["period"]), r["gen_tech"]
        e = float(r["Energy_GWh_typical_yr"] or 0)
        gen[p] = gen.get(p, 0) + e
        c = cat.setdefault(p, {})
        for k, hit in (("onshore", tech == "OnshoreWind"),
                       ("refuse", tech == "H-Power"),
                       ("egs", tech == "EGS"),
                       ("storage", "Battery" in tech),
                       ("cogen", tech in COGENS)):
            if hit:
                c[k] = c.get(k, 0) + e
    return served, gen, cat


def rps_target_fn():
    rows = [(int(r["year"]), float(r["rps_target"]))
            for r in csv.DictReader(open(REPO / "inputs_nlv2s/rps_targets.csv"))]
    return lambda p: max((t for y, t in rows if y <= p), default=0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", default=None)
    args = ap.parse_args()
    target = rps_target_fn()

    for plan, (src, family) in PLANS.items():
        if args.plan and plan != args.plan:
            continue
        shares = plan_grid_shares(src)
        served, gen, cat = solved(family, plan)
        q = {}
        for r in csv.DictReader(
                open(REPO / f"quotas/plan_quota_{plan}_{family}.csv")):
            q[(int(r["period"]), r["category"], r["bound"])] = float(r["gwh"])

        print(f"\n=== {plan} on {family} ===")
        print("\n(1) RPS: is the quota's fossil FLOOR above what the target allows?")
        print(f"  {'yr':<6}{'fossil min':>11}{'+cogens':>9}{'gen':>9}"
              f"{'non-ren':>9}{'allowed':>9}{'verdict':>12}")
        for p in PERIODS:
            if p not in served:
                continue
            fmin, cog, G = q.get((p, "fossil", "min")), cat[p].get("cogen", 0), gen[p]
            if fmin is None:
                print(f"  {p:<6}{'(none)':>11}{cog:>9.0f}{G:>9.0f}"
                      f"{'':>9}{1-target(p):>9.0%}{'unpinned':>12}")
                continue
            nonren, allowed = (fmin + cog) / G, 1 - target(p)
            ok = nonren <= allowed
            print(f"  {p:<6}{fmin:>11.0f}{cog:>9.0f}{G:>9.0f}{nonren:>9.1%}"
                  f"{allowed:>9.0%}{'ok' if ok else 'VIOLATES':>12}")

        print("\n(2) Energy balance: how much room do the ceilings leave?"
              "\n    (a squeeze here is the mechanism, not the test -- the test"
              "\n     is the elastic solve, which sheds discretionary load)")
        for p in PERIODS:
            if p not in served or (p, "fossil", "max") not in q:
                continue          # only periods with every ceiling in force
            L, G, c = served[p], gen[p], cat[p]
            ledger = [("usolar   quota max", q[(p, "usolar", "max")]),
                      ("offshore quota max", q.get((p, "offshore", "max"), 0)),
                      ("fossil   quota max", q[(p, "fossil", "max")]),
                      ("onshore  150 MW cap", c.get("onshore", 0)),
                      ("refuse   86 MW cap", c.get("refuse", 0)),
                      ("EGS      100 MW cap", c.get("egs", 0)),
                      ("cogens   must-run", c.get("cogen", 0)),
                      ("storage  net", c.get("storage", 0))]
            avail = sum(v for _, v in ledger)
            print(f"\n  {p}: ceilings and caps supply {avail:,.0f} GWh against "
                  f"{L:,.0f} GWh of load")
            for k, v in ledger:
                print(f"      {k:<22}{v:>9,.0f}")
            print(f"      {'available':<22}{avail:>9,.0f}")
            # The cell's own generation is NOT the requirement: electrolysis
            # draw and storage cycling are discretionary, and a squeezed cell
            # sheds them. Quoting G as a requirement overstates the gap -- it
            # reports 2035 as short by 376 GWh when 2035 in fact solves. The
            # binding number is the minimum violation from the elastic solve
            # (plan_mix_quota_elastic), which sheds everything sheddable.
            print(f"      for reference the unsqueezed cell generates {G:,.0f}, "
                  f"of which {G - L:,.0f} is losses, storage and electrolysis")
            for k, why in HARD_CAPPED.items():
                gap = shares[p][k] * L - c.get(k, 0)
                print(f"      note: plan's {k} share wants "
                      f"{shares[p][k]*L:,.0f}, {why} delivers "
                      f"{c.get(k, 0):,.0f}  (short {gap:,.0f})")


if __name__ == "__main__":
    main()

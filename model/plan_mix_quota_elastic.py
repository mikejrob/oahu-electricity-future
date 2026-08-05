"""Diagnostic twin of plan_mix_quota: which band makes a plan unreachable?

Include this module INSTEAD of plan_mix_quota when a pinned-mix cell comes
back infeasible. It builds the same quota rows, but each one carries a
non-negative slack variable, and the objective becomes the total slack
(MWh) rather than system cost. Every run is therefore feasible, and the
solution reports the smallest violation that makes the plan reachable:
which period, which category, which side of the band, and by how much.

That last number is the point. "The 2045 utility-solar ceiling is
infeasible" is not actionable; "the 2045 utility-solar ceiling has to rise
from 2,487.8 to 3,140 GWh, or nothing else moves" tells the author exactly
what loosening the band would cost in fidelity to the plan.

Switch ships switch_model.balancing.diagnose_infeasibility, which does this
for the whole model. It is not usable here: it relaxes every constraint
(millions of slacks on this model) and its convert_bounds_to_constraint()
returns a hard-coded m.BuildGen["S-Geothermal", 2020] left over from
debugging, so variable bounds come out attached to the wrong variable.
Relaxing only the ~24 quota rows is both correct and far smaller.

Use --quota-hard to hold rows fixed while the rest stay elastic, the same
way that module's --no-relax works: if holding the 2040 fossil ceiling hard
pushes the violation onto the 2045 solar ceiling, the two are in conflict.
Rows are named period:category:bound, e.g. --quota-hard 2040:fossil:max.

Results from this module are diagnostic only — the dispatch it reports
minimizes violation, not cost, so no cell solved with it belongs in the
report. Once the bands are settled, re-solve with plan_mix_quota.
"""
import csv
import os

from pyomo.environ import (Constraint, NonNegativeReals, Objective, Set, Var,
                           minimize, value)

# Mirrors plan_mix_quota.CAT_SOURCES and its gens()/annual_mwh() logic. Kept
# as a copy rather than an import so that the module the published cells are
# solved with is never edited to serve a diagnostic.
CAT_SOURCES = ("LSFO", "Diesel", "LNG", "multiple")


def define_arguments(argparser):
    argparser.add_argument("--plan-quota-file", default=None,
                           help="CSV of generation quotas (period, category, "
                                "bound, gwh); omit to disable")
    argparser.add_argument("--plan-quota-fossil-exempt", default="",
                           help="comma-separated name substrings of projects "
                                "excluded from the fossil quota")
    argparser.add_argument("--quota-hard", nargs="+", default=[],
                           help="quota rows to leave un-relaxed, named "
                                "period:category:bound (e.g. 2040:fossil:max); "
                                "the run is infeasible if these alone cannot "
                                "be met, which is itself the answer")


def _row_name(p, cat, bound):
    return f"{p}:{cat}:{bound}"


def define_components(m):
    if not getattr(m.options, "plan_quota_file", None):
        return
    with open(m.options.plan_quota_file) as f:
        quotas = [(int(r["period"]), r["category"], r["bound"],
                   float(r["gwh"])) for r in csv.DictReader(f)]
    m._plan_quotas = quotas

    def gens(m, cat):
        if cat == "usolar":
            return [g for g in m.GENERATION_PROJECTS
                    if "CentralTrackingPV" in g]
        if cat == "offshore":
            return [g for g in m.GENERATION_PROJECTS
                    if m.gen_tech[g] == "OffshoreWind"]
        if cat == "wind":
            return [g for g in m.GENERATION_PROJECTS
                    if m.gen_tech[g] in ("OffshoreWind", "OnshoreWind")]
        if cat == "fossil":
            exempt = [s for s in
                      getattr(m.options, "plan_quota_fossil_exempt", "").split(",")
                      if s]
            return [g for g in m.GENERATION_PROJECTS
                    if m.gen_energy_source[g] in CAT_SOURCES
                    and not m.gen_is_baseload[g]
                    and not any(s in g for s in exempt)]
        raise ValueError(cat)

    def fuel_cell_mwh(m, p):
        return sum(m.DispatchFuelCellMW[z, t] * m.tp_weight_in_year[t]
                   for z in m.LOAD_ZONES for t in m.TPS_IN_PERIOD[p])

    def annual_mwh(m, p, cat):
        if cat == "hydrogen":
            return fuel_cell_mwh(m, p)
        if cat == "firm":
            return fuel_cell_mwh(m, p) + annual_mwh(m, p, "fossil")
        return sum(m.DispatchGen[g, t] * m.tp_weight_in_year[t]
                   for g in gens(m, cat) for t in m.TPS_IN_PERIOD[p]
                   if (g, t) in m.GEN_TPS)

    m.PLAN_QUOTA_ROWS = Set(initialize=list(range(len(quotas))),
                            dimen=1, ordered=True)

    # one slack per row, in the direction that row can be missed: a floor can
    # only be undershot, a ceiling only overshot
    m.PlanQuotaSlack = Var(m.PLAN_QUOTA_ROWS, within=NonNegativeReals,
                           initialize=0.0)

    hard = set(m.options.quota_hard)
    m._plan_quota_hard = hard

    def quota_rule(m, i):
        p, cat, bound, gwh = quotas[i]
        if p not in m.PERIODS:
            return Constraint.Skip
        # same guard as plan_mix_quota: a pre-check that accepted a firm row
        # the production module rejects would be worse than useless
        if cat == "firm":
            tgt = getattr(m, "rps_target_for_period", None)
            if tgt is None or tgt[p] != 1.0:
                raise ValueError(
                    f"firm quota at {p} with RPS target "
                    f"{'none' if tgt is None else tgt[p]}, not 1.0")
        expr = annual_mwh(m, p, cat)
        slack = 0.0 if _row_name(p, cat, bound) in hard else m.PlanQuotaSlack[i]
        if bound == "min":
            return expr + slack >= gwh * 1000.0
        return expr - slack <= gwh * 1000.0

    m.Plan_Mix_Quota = Constraint(m.PLAN_QUOTA_ROWS, rule=quota_rule)

    unknown = hard - {_row_name(p, c, b) for p, c, b, _ in quotas}
    if unknown:
        raise ValueError(f"--quota-hard names rows not in "
                         f"{m.options.plan_quota_file}: {sorted(unknown)}")
    print(f"Plan mix quotas active (ELASTIC): {len(quotas)} rows from "
          f"{m.options.plan_quota_file}; {len(hard)} held hard")


def define_dynamic_components(m):
    if not getattr(m.options, "plan_quota_file", None):
        return
    # minimize total violation instead of system cost: the cheapest-cost
    # answer is meaningless once the model is infeasible, and carrying the
    # cost objective alongside a penalty just makes the LP harder without
    # changing which rows have to give
    m.Total_Plan_Quota_Violation = Objective(
        rule=lambda m: sum(m.PlanQuotaSlack[i] for i in m.PLAN_QUOTA_ROWS),
        sense=minimize)


def pre_solve(m):
    if getattr(m.options, "plan_quota_file", None):
        m.Minimize_System_Cost.deactivate()


def post_solve(m, outputs_dir):
    if not getattr(m.options, "plan_quota_file", None):
        return
    rows = []
    for i in m.PLAN_QUOTA_ROWS:
        p, cat, bound, gwh = m._plan_quotas[i]
        if p not in m.PERIODS:
            continue
        v = value(m.PlanQuotaSlack[i]) or 0.0
        gwh_slack = v / 1000.0
        # what the band would have to become for this row to hold
        needed = gwh - gwh_slack if bound == "min" else gwh + gwh_slack
        rows.append({"period": p, "category": cat, "bound": bound,
                     "quota_gwh": round(gwh, 1),
                     "violation_gwh": round(gwh_slack, 1),
                     "needed_gwh": round(needed, 1),
                     "hard": int(_row_name(p, cat, bound) in m._plan_quota_hard)})

    path = os.path.join(outputs_dir, "plan_quota_violations.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    binding = [r for r in rows if r["violation_gwh"] > 0.05]
    if binding:
        print(f"\nPLAN QUOTA INFEASIBLE: {len(binding)} row(s) must give; "
              f"total violation "
              f"{sum(r['violation_gwh'] for r in binding):.1f} GWh")
        for r in binding:
            print(f"  {r['period']} {r['category']:<9} {r['bound']:<3} "
                  f"{r['quota_gwh']:>8.1f} GWh -> needs {r['needed_gwh']:>8.1f} "
                  f"({r['violation_gwh']:+.1f})")
    else:
        print("\nPLAN QUOTA FEASIBLE: every row met with zero slack; the "
              "infeasibility is outside the quota set.")
    print(f"wrote {path}\n")

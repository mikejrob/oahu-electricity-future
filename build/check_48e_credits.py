#!/usr/bin/env python3
"""check_48e_credits.py -- sweep every input dir for correct 48E credit placement.

Policy (base case = current law, commit 5d79154): utility-scale storage
(Battery_Bulk/Conting/Reg) and Oahu_EGS carry x0.70 capital for build years
2027-2035 and FULL price from 2040 (post-expiry). Distributed batteries are
never credited (customer-side economics). gen_build_costs_noitc.csv is the
pre-credit table.

Per directory carrying a noitc file, this asserts:
  1. WINDOW    base = 0.70 x noitc on {Battery_Bulk, Conting, Reg, EGS} x
               {2027, 2030, 2035}, capital and storage-energy columns.
  2. EXPIRY    base == noitc on those projects for 2040+ (credit gone).
  3. SCOPE     base == noitc on every other row (DistBattery, predetermined
               vintages, all other projects -- nothing else credited).
  4. VARIANTS  pv15/pv17/jera120/noitc_jera120 carry the same battery+EGS
               rows as their parent (credit inherited, JERA rows aside);
               egs_low/high carry base battery rows and EGS rows equal to
               0.70 x the case trajectory in the window, full price after.
Directories without a noitc file are reported as LEGACY with their raw
2030 battery capital so staleness is visible, not asserted.

Usage: python build/check_48e_credits.py            (sweep, exit 1 on FAIL)
"""
import csv, glob, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "build"))

CREDITED = ("Oahu_Battery_Bulk", "Oahu_Battery_Conting", "Oahu_Battery_Reg",
            "Oahu_EGS")
WINDOW = {"2027", "2030", "2035"}
MONEY = ("gen_overnight_cost", "gen_storage_energy_overnight_cost")


def rows(path):
    return {(r["GENERATION_PROJECT"], r["build_year"]): r
            for r in csv.DictReader(open(path))}


def money_eq(a, b, ratio=1.0):
    for c in MONEY:
        if c not in a:
            continue
        if a[c] in (".", "") or b[c] in (".", ""):
            if a[c] != b[c]:
                return False
            continue
        if abs(float(a[c]) - ratio * float(b[c])) > 0.02:
            return False
    return True


def check_dir(d):
    base_p, noitc_p = d / "gen_build_costs.csv", d / "gen_build_costs_noitc.csv"
    if not base_p.exists():
        return None
    if not noitc_p.exists():
        b = rows(base_p)
        v = b.get(("Oahu_Battery_Bulk", "2030"), {}).get("gen_overnight_cost", "?")
        return f"LEGACY (no noitc file; Battery_Bulk 2030 = {v})"
    base, noitc = rows(base_p), rows(noitc_p)
    errs = []
    if set(base) != set(noitc):
        errs.append("row sets differ between base and noitc")
    for k, rb in base.items():
        rn = noitc.get(k)
        if rn is None:
            continue
        in_win = k[0] in CREDITED and k[1] in WINDOW
        if in_win:
            if not money_eq(rb, rn, ratio=0.70):
                errs.append(f"WINDOW not 0.70x: {k}")
        else:
            if not money_eq(rb, rn):
                errs.append(f"{'EXPIRY' if k[0] in CREDITED else 'SCOPE'} "
                            f"differs from noitc: {k}")
    # variants inherit the credited rows
    for name, parent in (("gen_build_costs_pv15.csv", base_p),
                         ("gen_build_costs_pv17.csv", base_p),
                         ("gen_build_costs_jera120.csv", base_p),
                         ("gen_build_costs_noitc_jera120.csv", noitc_p)):
        vp = d / name
        if not vp.exists():
            continue
        var, par = rows(vp), rows(parent)
        if set(var) != set(par):
            errs.append(f"{name}: row set differs from parent")
        for g in CREDITED:
            for k in [k for k in par if k[0] == g]:
                if k in var and not money_eq(var[k], par[k]):
                    errs.append(f"{name}: {k} differs from parent")
    try:
        from build_corrected_inputs import egs_costs
        for tag in ("low", "high"):
            vp = d / f"gen_build_costs_egs_{tag}.csv"
            if not vp.exists():
                continue
            var = rows(vp)
            traj = {str(yr): float(ocst) for (yr, ocst, _f) in egs_costs(tag)}
            for k, rv in var.items():
                if k[0] == "Oahu_EGS" and k[1] in traj:
                    want = traj[k[1]] * (0.70 if k[1] in WINDOW else 1.0)
                    if abs(float(rv["gen_overnight_cost"]) - want) > 0.02:
                        errs.append(f"egs_{tag} EGS {k[1]}: "
                                    f"{rv['gen_overnight_cost']} want {want:.2f}")
                elif k[0] in CREDITED and k in var and k in rows(base_p):
                    if not money_eq(rv, rows(base_p)[k]):
                        errs.append(f"egs_{tag}: battery row {k} != base")
    except ImportError as e:
        errs.append(f"could not import egs_costs ({e}); EGS variant "
                    "trajectories unchecked")
    return errs


def main():
    dirs = sorted(p for p in REPO.glob("inputs*") if p.is_dir())
    assert dirs, "no inputs* dirs found — run from a checkout with inputs"
    failed = False
    for d in dirs:
        res = check_dir(d)
        if res is None:
            continue
        if isinstance(res, str):
            print(f"  {d.name:48s} {res}")
        elif res:
            failed = True
            print(f"  {d.name:48s} FAIL ({len(res)}):")
            for e in res[:6]:
                print(f"      {e}")
        else:
            print(f"  {d.name:48s} PASS (window x0.70, expiry full, scope, variants)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

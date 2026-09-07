#!/usr/bin/env python3
"""repair_egs_variant_credits.py -- one-time repair of external-audit finding 2.

The EGS cost-sensitivity alias files (gen_build_costs_egs_{low,high}[_jera120]
.csv) were derived from the PRE-credit base table, so they price utility-scale
batteries at 1/0.70 of the base in build years 2027/2030/2035 -- the 48E
storage-credit window. The EGS rows in those files are correct.

Repair: rebuild each variant as its base table (gen_build_costs.csv, or
gen_build_costs_jera120.csv for the _jera120 variants) with the Oahu_EGS rows
taken unchanged from the existing variant file. Assertions:

  * every non-EGS row of the repaired file equals the base row;
  * every Oahu_EGS row equals the pre-repair variant row;
  * the set of rows the repair CHANGES is exactly
    {Battery_Bulk, Battery_Conting, Battery_Reg} x {2027, 2030, 2035},
    each changed by the factor 0.70 -- anything else aborts the run.

Idempotent: re-running on repaired files changes nothing.

Usage: python build/repair_egs_variant_credits.py [--check-only]
"""
import csv, glob, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EXPECT_GENS = {"Oahu_Battery_Bulk", "Oahu_Battery_Conting", "Oahu_Battery_Reg"}
EXPECT_YEARS = {"2027", "2030", "2035"}
CREDIT = 0.70


def read(path):
    with open(path) as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def repair(var_path, check_only):
    d = var_path.parent
    base_name = ("gen_build_costs_jera120.csv"
                 if var_path.name.endswith("_jera120.csv")
                 else "gen_build_costs.csv")
    h, base = read(d / base_name)
    h2, old = read(var_path)
    assert h == h2, (var_path, "header mismatch")
    gp, by = h.index("GENERATION_PROJECT"), h.index("build_year")

    egs_old = {r[by]: r for r in old if r[gp] == "Oahu_EGS"}
    new, changed = [], []
    old_by_key = {(r[gp], r[by]): r for r in old}
    for r in base:
        nr = egs_old.get(r[by], r) if r[gp] == "Oahu_EGS" else r
        new.append(nr)
        o = old_by_key.get((nr[gp], nr[by]))
        if o is not None and o != nr:
            changed.append((nr[gp], nr[by], o, nr))

    for g, y, o, n in changed:
        assert g in EXPECT_GENS and y in EXPECT_YEARS, \
            f"{var_path}: unexpected change {g}/{y}: {o} -> {n}"
        for col in range(len(h)):
            if o[col] not in (".", "") and o[col] != n[col]:
                ratio = float(n[col]) / float(o[col])
                assert abs(ratio - CREDIT) < 1e-6, \
                    f"{var_path}: {g}/{y} col {h[col]} ratio {ratio}"

    if check_only or not changed:
        return len(changed)
    with open(var_path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(h)
        w.writerows(new)
    return len(changed)


def main():
    check_only = "--check-only" in sys.argv
    # "inputs_*" alone misses the root inputs/ directory (no underscore) —
    # that gap left the root's variants unrepaired on the first pass
    files = sorted(glob.glob(str(REPO / "inputs_*" / "gen_build_costs_egs_*.csv"))
                   + glob.glob(str(REPO / "inputs" / "gen_build_costs_egs_*.csv")))
    total, touched = 0, 0
    for p in files:
        n = repair(Path(p), check_only)
        total += n
        touched += bool(n)
        if n:
            print(f"  {'would fix' if check_only else 'fixed':10s} "
                  f"{Path(p).parent.name}/{Path(p).name}: {n} rows")
    print(f"{'CHECK' if check_only else 'REPAIR'}: {len(files)} variant files, "
          f"{touched} with uncredited battery rows, {total} rows total")
    return 1 if (check_only and touched) else 0


if __name__ == "__main__":
    sys.exit(main())

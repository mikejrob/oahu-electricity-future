#!/usr/bin/env python3
"""sanity_check_results.py — catch logically-impossible or missing solves
before any number is written into the report.

Every check encodes a relationship that MUST hold if the solves are correct.
A violation means a bad solve (non-converged / stuck MIP) or a missing cell,
not a real result. Run after any re-solve; fix flagged cells before trusting
the numbers. Exit 0 = clean, 1 = violations found.

Usage:  python sanity_check_results.py [--p001]   (default: 0.25% outputs_)
"""
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
PFX = "outputs_p001_" if "--p001" in sys.argv else "outputs_"
BR = ["lowbrent", "refbrent", "highbrent"]
viol, missing = [], []


def cost(name):
    p = REPO / f"{PFX}{name}" / "total_cost.txt"
    if not p.exists():
        missing.append(name)
        return None
    return float(p.read_text()) / 1e9


def egs_mw(name):
    f = REPO / f"{PFX}{name}" / "BuildGen.csv"
    if not f.exists():
        return None
    return sum(float(r[-1]) for r in csv.reader(open(f)) if "EGS" in r[0])


def check(cond, msg):
    if cond is None:
        return
    if not cond:
        viol.append(msg)


for br in BR:
    nt = cost(f"C4_NOTHERMAL_{br}")
    # 1. LSFO ladder monotone increasing in size (bigger oversized plant costs more)
    l = [cost(f"C{i}_LSFO250_{br}") if i == 1 else cost(f"C{i}_LSFO{s}_{br}")
         for i, s in [(1, 250), (2, 375), (3, 500)]]
    if all(x is not None for x in l):
        check(l[0] <= l[1] <= l[2] + 1e-6,
              f"[{br}] LSFO ladder not monotone: {l[0]:.3f} {l[1]:.3f} {l[2]:.3f}")
    # 2. JERA +20% must cost >= bare-EPC (same scenario, higher capital)
    for base in ("wb_C6_LNG500", "C5_LNG375", "C6_STATUSQUO"):
        b, j = cost(f"{base}_{br}"), cost(f"{base}_{br}_j120")
        if b is not None and j is not None:
            check(j >= b - 1e-6, f"[{br}] {base}: +20% ({j:.3f}) < bare ({b:.3f})")
    # 3. Any Waiau-containing bundle must exceed its Waiau-free counterpart
    wr = cost(f"wr_C4_NOTHERMAL_{br}")
    if wr is not None and nt is not None:
        check(wr >= nt, f"[{br}] Waiau ({wr:.3f}) < no-new-plant ({nt:.3f})")

# 4. EGS is bang-bang (0 or 100 MW): evaluate both corners directly rather than
#    let the solver agonize over a degenerate marginal decision. The low/high
#    sensitivity cells are solved with EGS PINNED at 100 MW (gen_info_egs100),
#    so their cost is the forced-100 cost at that EGS price. Two things must hold:
#    (a) forced-100 cost is monotone increasing in EGS price (same 100 MW build,
#        higher unit cost -> higher total): low <= ref <= high.
#    (b) EGS VALUE at each price = egs_none - forced100 (negative => don't build).
en = cost("egs_none_no_lng_refbrent")   # EGS=0 corner
er = cost("egs_ref_no_lng_refbrent")    # forced-100 at ref price (built 100 naturally)
eh = cost("egs_high_no_lng_refbrent")   # forced-100 at high price (pinned)
el = cost("egs_low_no_lng_refbrent")    # forced-100 at low price (pinned)
for tag, c in (("high", eh), ("ref", er), ("low", el)):
    mw = egs_mw(f"egs_{tag}_no_lng_refbrent")
    if mw is not None:
        check(mw > 99, f"EGS {tag}: pinned build is {mw:.0f}MW, expected 100 (bang-bang corner)")
if None not in (er, eh, el):
    check(el <= er + 1e-6, f"EGS forced-100 not monotone: egs_low_no_lng_refbrent ({el:.3f}) > ref ({er:.3f})")
    check(er <= eh + 1e-6, f"EGS forced-100 not monotone: egs_high_no_lng_refbrent bound - ref ({er:.3f}) > high ({eh:.3f})")
    # report the bang-bang readout (value = none - forced100; build 100 iff value>0)
    if en is not None:
        note = " | ".join(f"{t}:val={en-c:+.2f}({'build' if en-c>0 else 'skip'})"
                          for t, c in (("low", el), ("ref", er), ("high", eh)))
        print(f"  EGS bang-bang (ref oil, none={en:.2f}): {note}")

# 5. base no-new-plant must equal egs_ref (identical solution when thermal blocked
#    options are uneconomic) within solver tolerance
ntr = cost("C4_NOTHERMAL_refbrent")
if ntr is not None and er is not None:
    check(abs(ntr - er) < 0.05, f"C4_NOTHERMAL_ref ({ntr:.3f}) != egs_ref ({er:.3f}) by >0.05")

# 6. baseline monotone in oil price (higher oil -> higher no-new-plant cost)
nts = [cost(f"C4_NOTHERMAL_{b}") for b in BR]
if all(x is not None for x in nts):
    check(nts[0] <= nts[1] <= nts[2] + 1e-6,
          f"no-new-plant not monotone in oil: {nts[0]:.3f} {nts[1]:.3f} {nts[2]:.3f}")

# =====================================================================
# 7. COMPREHENSIVE STRICT-DOMINANCE SWEEP over the full solved set.
# Each rule pairs a cell with a version of itself that differs in exactly
# one cost input made MORE expensive; the cheaper cell must cost <= dearer.
# Any inversion is a stuck/suboptimal solve (the "cheaper" one over-solved).
# This catches degeneracy-induced bad incumbents anywhere, not just headline.
# =====================================================================
import glob as _glob
_all = {}
for _p in _glob.glob(str(REPO / f"{PFX}*" / "total_cost.txt")):
    _n = _p.split(f"{PFX}", 1)[1].rsplit("/", 1)[0]
    try:
        _all[_n] = float(open(_p).read()) / 1e9
    except Exception:
        pass

def _dom(cheaper, dearer, why, tol=0.002):
    # tol: 0.25% solver gap can put a dearer cell slightly under; flag only
    # inversions bigger than ~2x the gap (a real stuck solve, not gap slop).
    if cheaper in _all and dearer in _all and _all[cheaper] > _all[dearer] + tol:
        viol.append(f"DOMINANCE {why}: {cheaper} ({_all[cheaper]:.3f}) > {dearer} ({_all[dearer]:.3f})")

_dompairs = 0
for _n in list(_all):
    # (a) bare-EPC <= +20% capital (identical but JERA capital x1.2)
    if not _n.endswith("_j120") and f"{_n}_j120" in _all:
        _dom(_n, f"{_n}_j120", "bare<=+20%"); _dompairs += 1
    # (b) Advanced renewables <= baseline renewables (adv is strictly cheaper)
    if _n.endswith("_adv") and _n[:-4] in _all:
        _dom(_n, _n[:-4], "adv<=baseline"); _dompairs += 1
    # (c) solar-premium ordering: pv15 <= pv17 (identical but higher premium)
    if _n.startswith("be_pv15_") and ("be_pv17_" + _n[8:]) in _all:
        _dom(_n, "be_pv17_" + _n[8:], "pv15<=pv17"); _dompairs += 1

print(f"  dominance sweep: {_dompairs} pairs checked across {len(_all)} solved cells")

print(f"== sanity check ({PFX}) ==")
if missing:
    print(f"MISSING ({len(missing)}): " + ", ".join(sorted(set(missing))[:25]))
if viol:
    print(f"VIOLATIONS ({len(viol)}):")
    for v in viol:
        print("  " + v)
if not missing and not viol:
    print("clean — no impossible or missing solves among checked cells")
# emit the flagged cell names for the barrier-resolve driver
_flag = sorted(set(missing) | {v.split(":")[1].split("(")[0].strip()
               for v in viol if ":" in v and "(" in v})
if _flag:
    open("/tmp/sanity_flagged.txt","w").write("\n".join(_flag)+"\n")
sys.exit(1 if (viol or missing) else 0)

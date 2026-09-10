#!/usr/bin/env python3
"""sanity_check_results.py — catch logically-impossible or missing solves
before any number is written into the report.

Every check encodes a relationship that MUST hold if the solves are correct.
A violation means a bad solve (non-converged / stuck MIP) or a missing cell,
not a real result. Run after any re-solve; fix flagged cells before trusting
the numbers. Exit 0 = clean, 1 = violations found.

Usage:  python sanity_check_results.py [--p001|--first-pass]
        default: the PUBLISHED basis — best available refinement per cell
        (R010_ > R0015_ > outputs_), the same resolution the analysis
        scripts use. --first-pass restricts to the 0.25% outputs_ dirs.
        The fuel-curve alias bug of Aug 2026 sat visible to this check for
        four days while it was only run by hand; push_both.sh now runs it
        as a hard gate, on the published basis, so a dominance violation
        cannot reach the public repository again.
"""
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
FIRST_PASS = "--first-pass" in sys.argv
PFX = "outputs_p001_" if "--p001" in sys.argv else "outputs_"
BR = ["lowbrent", "refbrent", "highbrent"]
viol, missing = [], []

# The EGS cost-sensitivity corners were DERIVED on the old fleet (a
# capital reprice off the clean egs_none/egs_ref cells — SOLVER_NOTES.md);
# the corrected fleet solves the low corner directly. Solved cells are
# checked for monotonicity; an absent corner is not a missing solve.
OPTIONAL = {"egs_high_no_lng_refbrent", "egs_low_no_lng_refbrent"}


def cost(name):
    if name in OPTIONAL:
        return cost_optional(name)
    if not FIRST_PASS and PFX == "outputs_":
        for pre in ("R010_outputs_", "R0015_outputs_", "outputs_"):
            p = REPO / f"{pre}{name}" / "total_cost.txt"
            if p.exists():
                return float(p.read_text()) / 1e9
        missing.append(name)
        return None
    p = REPO / f"{PFX}{name}" / "total_cost.txt"
    if not p.exists():
        missing.append(name)
        return None
    return float(p.read_text()) / 1e9


def cost_optional(name):
    for pre in ("R010_outputs_", "R0015_outputs_", "outputs_"):
        p = REPO / f"{pre}{name}" / "total_cost.txt"
        if p.exists():
            return float(p.read_text()) / 1e9
    return None


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
# one cost input made MORE expensive; the cheaper cell must cost <= dearer
# (raising a cost coefficient cannot lower a minimum). Any larger inversion
# is a stuck/suboptimal solve (the "cheaper" one over-solved).
#
# Until 2026-09-06 this sweep globbed only the first-pass outputs_* dirs —
# bypassing the R010>R0015>outputs published basis that cost() implements
# and the banner below advertises — matched premium pairs only on legacy
# unprefixed names, and used a flat $2M tolerance that its comment
# misdescribed as "~2x the gap" (external-audit finding 4). It now sweeps
# the same basis as every other check, at the only defensible tolerance:
# one proven optimality gap of the CHEAPER cell (the dearer incumbent
# already bounds its optimum from above, so only the cheaper cell's gap
# can produce a legitimate inversion).
# =====================================================================
import glob as _glob
_PREFIX_GAP = (("R010_outputs_", 0.001), ("R0015_outputs_", 0.0015),
               ("outputs_", 0.0025))
if FIRST_PASS:
    _sweep_basis = (("outputs_", 0.0025),)
elif PFX != "outputs_":                       # --p001 legacy mode
    _sweep_basis = ((PFX, 0.001),)
else:
    _sweep_basis = _PREFIX_GAP
# achieved gaps, where the solver logs prove them, override the requested
# tier: 12 published cells hit the time limit above 0.1% (SOLVE_MANIFEST)
_achieved = {}
_mpath = REPO / "results" / "SOLVE_MANIFEST.csv"
if _mpath.exists():
    for _r in csv.DictReader(open(_mpath)):
        if _r["relmipgap_achieved"]:
            _achieved[_r["outputs_dir"]] = float(_r["relmipgap_achieved"])

_all = {}                                     # name -> (cost_B, proven gap)
for _pre, _gap in _sweep_basis:
    for _p in _glob.glob(str(REPO / f"{_pre}*" / "total_cost.txt")):
        _n = _p.split(_pre, 1)[1].rsplit("/", 1)[0]
        # outputs_* also matches legacy p001 and local test dirs — exclude
        if _n.startswith("p001_") or "battfix" in _n or _n in _all:
            continue
        try:
            _g = max(_gap, _achieved.get(f"{_pre}{_n}", 0.0))
            _all[_n] = (float(open(_p).read()) / 1e9, _g)
        except Exception:
            pass

def _dom(cheaper, dearer, why):
    if cheaper not in _all or dearer not in _all:
        return
    (cc, gc), (cd, _gd) = _all[cheaper], _all[dearer]
    if cc > cd + gc * cd:                     # beyond the cheaper cell's gap
        viol.append(f"DOMINANCE {why}: {cheaper} ({cc:.3f}) > {dearer} ({cd:.3f})")

_dompairs = {"bare<=+20%": 0, "adv<=baseline": 0, "pv15<=pv17": 0}
for _n in list(_all):
    # (a) bare-EPC <= +20% capital (identical but JERA capital x1.2)
    if not _n.endswith("_j120") and f"{_n}_j120" in _all:
        _dom(_n, f"{_n}_j120", "bare<=+20%"); _dompairs["bare<=+20%"] += 1
    # (b) Advanced renewables <= baseline renewables. NOTE: a true identity
    # only while the _adv inputs differ from baseline SOLELY by cheaper
    # technology costs — restored by the 2026-09-06 advsolar credit fix.
    if _n.endswith("_adv") and _n[:-4] in _all:
        _dom(_n, _n[:-4], "adv<=baseline"); _dompairs["adv<=baseline"] += 1
    # (c) solar-premium ordering: pv15 <= pv17 (identical but higher premium);
    # substring match covers the family-prefixed published names
    if "be_pv15_" in _n and _n.replace("be_pv15_", "be_pv17_") in _all:
        _dom(_n, _n.replace("be_pv15_", "be_pv17_"), "pv15<=pv17")
        _dompairs["pv15<=pv17"] += 1

# a rule that matches nothing is a broken rule, not a passing one
if not FIRST_PASS and PFX == "outputs_":
    for _why, _npairs in _dompairs.items():
        if _npairs == 0 and _all:
            viol.append(f"DOMINANCE sweep: rule '{_why}' matched ZERO pairs "
                        f"across {len(_all)} cells — pairing logic broken")
print(f"  dominance sweep: {sum(_dompairs.values())} pairs "
      f"({', '.join(f'{k}={v}' for k, v in _dompairs.items())}) "
      f"across {len(_all)} cells on the swept basis")
# A green gate that swept nothing verified nothing: on a partial checkout
# the MISSING branch fires first, but if outputs were ever partially
# synced past it, this floor keeps the gate honest about coverage
# (2026-09-08 audit note; full fleet sweeps ~1,100+ cells / 600+ pairs).
if sum(_dompairs.values()) < 400 or len(_all) < 800:
    print(f"FAIL: dominance sweep coverage below floor "
          f"({sum(_dompairs.values())} pairs / {len(_all)} cells; "
          f"need >=400 / >=800) — refusing to pass on a sliver")
    raise SystemExit(1)

print(f"== sanity check ({'first-pass ' + PFX if FIRST_PASS or PFX != 'outputs_' else 'published basis: R010>R0015>outputs'}) ==")
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

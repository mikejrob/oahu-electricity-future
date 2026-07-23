#!/usr/bin/env python3
"""
build_brent_variants.py
=======================
Build REAL-dollar low/high Brent fuel-price sensitivity curves, replacing the
published NOMINAL-Brent variants (the convention error documented in
docs/FUEL_CONVENTION.md).

REFERENCE Brent is NOT rebuilt: the reference case uses the base
fuel_supply_curves.csv in each input dir, which build_corrected_inputs.py has
already deflated to real 2024$ (Ethan's pipeline expressed it in 2027$; we take
it back to 2024$ so the whole model shares one dollar unit).  The AEO2025 case
anchors below are themselves real 2024$, so the fan is dollar-year-consistent.
This script only produces the low/high brackets around that real reference.

METHOD (fully disclosed; every external number is verified in SOURCES.md)
  1. For each period, take the real 2024$ reference LSFO and LNG ($/MMBtu).
  2. Invert LSFO to the implied real reference Brent using the published R3
     regression from mikejrob/hawaii-lng-lsfo-brief:
         LSFO_$/bbl = 0.7388 * Brent_$/bbl + 37.30 ; 6.22 MMBtu/bbl
  3. Apply the EIA AEO 2025 oil-price CASE SPREAD. Verified anchors (real
     2024$, AEO2025 narrative, 2050): Reference $91/bbl, Low $48/bbl,
     High $157/bbl  ->  case ratios low=48/91=0.5275, high=157/91=1.7253.
     The ratio is linearly interpolated from parity (1.0) at the 2027 model
     base year to the verified 2050 ratio. NOTE (disclosed): AEO cases already
     diverge before 2050; starting the fan at 2027 parity UNDERSTATES the
     near-term spread, so these brackets are conservative in early years.
  4. Apply the Brent shock to Ethan's exact reference via the regression
     SLOPES, so the reference is preserved to the cent at parity:
         LSFO_case = LSFO_ref + (0.7388/6) * (Brent_case - Brent_ref)
         LNG_case  = LNG_ref  + 0.118      * (Brent_case - Brent_ref)
     (LNG slope 0.118 $/MMBtu per $/bbl = HSEO/FGE indicative contract, per the
     brief; generous to LNG buyers vs the ~0.13 spot slope.)
  5. Other fuels scale by 1 + weight*(ratio-1): Diesel/Motor_Diesel/
     Motor_Gasoline weight 1.0, Biodiesel 0.3, Coal/Biomass 0.0 (as the report).

Output: inputs/fuel_supply_curves_lowbrent.csv
        inputs/fuel_supply_curves_highbrent.csv
"""
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent    # portable: repo root from script
import sys
INPUT_DIRS = sys.argv[1:] or ["inputs", "inputs_lu_constrained_c"]
# each input dir carries its own (identical, Ethan real-base) fuel_supply_curves.csv

LSFO_SLOPE, LSFO_INT, MMBTU_PER_BBL = 0.7388, 37.30, 6.22  # R3 regression + heat
#   content, Roberts (2026) hawaii-lng-lsfo-brief: LSFO $/bbl = 0.7388*Brent + 37.30;
#   6.22 MMBtu/bbl (residual fuel oil). LNG $/MMBtu = 0.118*Brent + 0.60.
LNG_SLOPE = 0.118                                            # HSEO/FGE contract

# Verified AEO2025 real-2024$ Brent, 2050 (AEO2025 narrative, p.3):
BRENT_2050 = {"ref": 91.0, "low": 48.0, "high": 157.0}
RATIO_2050 = {"low": BRENT_2050["low"] / BRENT_2050["ref"],     # 0.5275
              "high": BRENT_2050["high"] / BRENT_2050["ref"]}   # 1.7253
BASE_YEAR = 2027

OTHER_WEIGHT = {"Diesel": 1.0, "Motor_Diesel": 1.0, "Motor_Gasoline": 1.0,
                "Biodiesel": 0.3}   # else 0.0 (Coal, Pellet-Biomass, ...)


def case_ratio(year, case):
    r2050 = RATIO_2050[case]
    if year <= BASE_YEAR:
        return 1.0
    return 1.0 + (r2050 - 1.0) * (year - BASE_YEAR) / (2050 - BASE_YEAR)


def brent_from_lsfo(lsfo_mmbtu):
    return (lsfo_mmbtu * MMBTU_PER_BBL - LSFO_INT) / LSFO_SLOPE


def build(case, d):
    src = REPO / d / "fuel_supply_curves.csv"
    out = REPO / d / f"fuel_supply_curves_{case}brent.csv"
    with open(src, newline="") as fin, open(out, "w", newline="") as fout:
        r = csv.reader(fin)
        w = csv.writer(fout, lineterminator="\n")
        header = [c.replace("\r", "") for c in next(r)]
        w.writerow(header)
        FUEL, PERIOD, COST = (header.index("fuel"), header.index("period"),
                              header.index("unit_cost"))
        for row in r:
            row = [c.replace("\r", "") for c in row]
            if not row:
                continue
            try:
                yr = int(row[PERIOD]); ref = float(row[COST])
            except (ValueError, IndexError):
                w.writerow(row); continue
            ratio = case_ratio(yr, case)
            if row[FUEL] == "LSFO":
                brent_ref = brent_from_lsfo(ref)
                dbrent = brent_ref * (ratio - 1.0)
                row[COST] = f"{ref + (LSFO_SLOPE / MMBTU_PER_BBL) * dbrent:.6f}"
            elif row[FUEL] == "LNG":
                # Invert this row's reference LNG to its implied crude via the
                # LNG contract (LNG = 0.118*Brent + 0.60), apply the same case
                # ratio, and push back through the slope. Preserves the exact
                # reference LNG at parity; same proportional Brent move as LSFO.
                brent_ref = (ref - 0.60) / LNG_SLOPE
                dbrent = brent_ref * (ratio - 1.0)
                row[COST] = f"{ref + LNG_SLOPE * dbrent:.6f}"
            else:
                wt = OTHER_WEIGHT.get(row[FUEL], 0.0)
                row[COST] = f"{ref * (1.0 + wt * (ratio - 1.0)):.6f}"
            w.writerow(row)
    return out


def verify(d):
    def lsfo_by_year(path):
        d = {}
        with open(path, newline="") as f:
            r = csv.reader(f); h = [c.replace("\r", "") for c in next(f).split(",")]
        # simple reparse
        with open(path, newline="") as f:
            rd = csv.DictReader(f)
            for row in rd:
                if row["fuel"] == "LSFO":
                    d[int(row["period"])] = float(row["unit_cost"])
        return d
    ref = lsfo_by_year(REPO / d / "fuel_supply_curves.csv")
    lo = lsfo_by_year(REPO / d / "fuel_supply_curves_lowbrent.csv")
    hi = lsfo_by_year(REPO / d / "fuel_supply_curves_highbrent.csv")
    print("LSFO $/MMBtu by year (low < ref < high; equal at base year 2027):")
    ok = True
    for y in sorted(ref):
        tag = ""
        if y == BASE_YEAR:
            if not (abs(lo[y]-ref[y]) < 1e-6 and abs(hi[y]-ref[y]) < 1e-6):
                ok = False; tag = "  <- base year not preserved!"
        else:
            if not (lo[y] < ref[y] < hi[y]):
                ok = False; tag = "  <- ordering broken!"
        print(f"  {y}: low {lo[y]:6.2f}  ref {ref[y]:6.2f}  high {hi[y]:6.2f}{tag}")
    # check 2050 implied Brent hits verified anchors
    b_ref = brent_from_lsfo(ref[2050]); b_hi = brent_from_lsfo(hi[2050])
    print(f"\n2050 implied Brent: ref ${b_ref:.0f}/bbl (Ethan real), "
          f"high ${b_hi:.0f}/bbl (= ref x {RATIO_2050['high']:.3f})")
    assert ok, "brent variant verification failed"
    print("VERIFY: reference preserved at base year, low<ref<high elsewhere. OK")


if __name__ == "__main__":
    for d in INPUT_DIRS:
        print(f"--- {d} ---")
        for case in ("low", "high"):
            p = build(case, d)
            print("wrote", d + "/" + p.name)
        verify(d)

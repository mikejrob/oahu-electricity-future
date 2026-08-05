#!/usr/bin/env python
"""
verify_claims.py — re-derive every load-bearing number in the corrected inputs
from the vendored primary sources and assert it, on a bare clone (no external
ground truth needed). Exit 0 = every claim checks out. This is the gate: run it
before trusting the repo.

All costs are real 2024 US dollars (NPV valued as of 2027). Conventions are
documented in docs/CONVENTIONS.md; the load-bearing ones are re-derived here.
"""
import csv
import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
CPI = 1.027 ** 2            # 2022 -> 2024 US-CPI rebase for ATB 2024 (quoted in 2022$)
HAWAII = 1.20              # solar/battery capital premium (author floor)
PVB_SHARE = 0.5            # ATB 2024 PV-Plus-Battery config: 50 MW battery per 100 MW PV
FAILS = []


def ok(name, cond, detail=""):
    print(f"  [{'ok' if cond else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)


def atb(tech, td, par, scen="Moderate", year="2030"):
    for r in csv.DictReader(open(REPO / "sources" / "ATBe_2024_v3.0.0_slice.csv")):
        if (r["technology"] == tech and r["techdetail"] == td
                and r["core_metric_parameter"] == par and r["scenario"] == scen
                and r["core_metric_case"] == "Market" and r["crpyears"] == "20"
                and r["core_metric_variable"] == year):
            return float(r["value"]) * 1000        # $/kW -> $/MW
    return None


def cost(path, proj, year, col):
    for line in open(path, encoding="utf-8", errors="replace"):
        p = line.replace("\r", "").rstrip("\n").split(",")
        if len(p) > col and p[0] == proj and p[1] == year:
            return float(p[col])
    return None


GBC = REPO / "inputs" / "gen_build_costs.csv"

print("== SOURCE HASHES ==")
for f, pref in {"sources/ATBe_2024_v3.0.0_slice.csv": "11983d01",
                "sources/JERA_Proposal_State_of_Hawaii_March_17_2026.pdf": "e8ebd12c",
                "sources/EIA_AEO2025_narrative.pdf": "2d23f8fc"}.items():
    h = hashlib.sha256((REPO / f).read_bytes()).hexdigest()
    ok(f"{f} {pref}…", h.startswith(pref), h[:8])

print("\n== INPUT-SET COMPLETENESS ==")
for d in ("inputs", "inputs_lu_constrained_c"):
    for v in ("fuel_supply_curves.csv", "fuel_supply_curves_lowbrent.csv",
              "fuel_supply_curves_highbrent.csv", "gen_build_costs.csv",
              "gen_build_costs_egs_low.csv", "gen_build_costs_egs_high.csv"):
        ok(f"{d}/{v}", (REPO / d / v).exists())

print("\n== PRICE LEVEL: real 2024$ via 2.7%/yr CPI (2022->2024) on ATB 2024 ==")
sf = cost(GBC, "Oahu_CentralTrackingPV_Reference_wSlope_Flat_PV_01", "2030", 2)
tgt = atb("UtilityPV", "Class5", "CAPEX") * CPI * HAWAII
ok("solar Flat 2030 = ATB x1.0547 x1.20", abs(sf - tgt) / tgt < 1e-3, f"{sf:,.0f} vs {tgt:,.0f}")
sfom = cost(GBC, "Oahu_CentralTrackingPV_Reference_wSlope_Flat_PV_01", "2030", 4)
tfom = atb("UtilityPV", "Class5", "Fixed O&M") * CPI          # FOM: rebase only, no premium
ok("solar FOM 2030 = ATB FOM x1.0547 (no premium)", abs(sfom - tfom) / tfom < 1e-3, f"{sfom:,.0f} vs {tfom:,.0f}")

bp = cost(GBC, "Oahu_Battery_Bulk", "2030", 2)
be = cost(GBC, "Oahu_Battery_Bulk", "2030", 3)
btgt = (atb("Utility-Scale PV-Plus-Battery", "Class5", "CAPEX")
        - atb("UtilityPV", "Class5", "CAPEX")) / PVB_SHARE * CPI * HAWAII * 0.70   # ATB hybrid coloc, x0.70 48E credit (2030 vintage)
ok("battery 4h 2030 = ATB-PVB coloc x CPI x1.20 x0.70 (48E)", abs((bp + 4 * be) - btgt) / btgt < 1e-4, f"{bp+4*be:,.0f} vs {btgt:,.0f}")

print("\n== JERA plant-only (proposal p.30, 2026$ -> 2024$) ==")
j = cost(GBC, "Oahu_JERA", "2030", 2)
jtgt = 3_020_000 * (1.027 ** -2)
ok("JERA 2030 = $3,020k x1.027^-2 (2024$)", abs(j - jtgt) < 1, f"{j:,.0f} vs {jtgt:,.0f}")

print("\n== JERA part-load curve (CEMS-derived; sources/epa_cems/) ==")
jrows = [l.strip().split(",") for l in open(REPO / "inputs" / "gen_inc_heat_rates.csv")
         if l.startswith("Oahu_JERA")]
ok("JERA min load 62.5 MW, 476.0 MMBtu/h",
   jrows and jrows[0][1] == "62.5" and jrows[0][4] == "476.0")
ok("JERA incremental 6.225 through 125 MW",
   len(jrows) == 4 and all(r[3] == "6.225" for r in jrows[1:]) and jrows[-1][2] == "125.0")
ok("JERA full-load average = 6.92",
   abs((476.0 + 6.225 * 62.5) / 125 - 6.92) < 0.005)

print("\n== Waiau: HECO's STATED construction cost (system-cost basis, not recoverable) ==")
w = cost(GBC, "Oahu_Waiau_Repower", "2030", 2)
wtgt = 4_545_000.0                       # $1.155B / 253 MW; original report input
ok("Waiau = HECO stated $4,545/kW", abs(w - wtgt) < 1, f"{w:,.0f} vs {wtgt:,.0f}")

print("\n== EGS 2030 trio (2024$): 6 (GeoVision) / 10 (compromise) / 14.7 (ATB-Conservative shape) ==")
lo = cost(REPO / "inputs" / "gen_build_costs_egs_low.csv", "Oahu_EGS", "2030", 2)
rf = cost(GBC, "Oahu_EGS", "2030", 2)
hi = cost(REPO / "inputs" / "gen_build_costs_egs_high.csv", "Oahu_EGS", "2030", 2)
ok("EGS low 2030 = GeoVision $6.2M x0.70 (48E)", abs(lo - 6_200_000 * 0.70) < 1, f"{lo:,.0f}")
ok("EGS ref 2030 = $10M compromise x0.70 (48E)", abs(rf - 10_000_000 * 0.70) < 1, f"{rf:,.0f}")
ok("EGS high 2030 = $14.7M ATB-Conservative x0.70 (48E)", abs(hi - 14_700_000 * 0.70) < 1, f"{hi:,.0f}")

print("\n== fuel schedule: LSFO heat content 6.22 MMBtu/bbl (published brief) ==")
src = (REPO / "build" / "build_brent_variants.py").read_text()
ok("build_brent_variants uses 6.22", "6.22" in src and "6.0 " not in src.split("MMBTU_PER_BBL")[1][:30])

print("\n== SCENARIO COUNTS: 64 unique = 46 reference + 18 land-constrained ==")
import re
def names(f):
    return [re.search(r"--scenario-name (\S+)", l).group(1)
            for l in open(REPO / "scenarios" / f) if l.strip()]
ref, lc = names("scenarios_p025_reference.txt"), names("scenarios_p025_lc.txt")
ok("46 reference, unique", len(ref) == len(set(ref)) == 46, str(len(ref)))
ok("18 land-constrained, unique", len(lc) == len(set(lc)) == 18, str(len(lc)))

print("\n== COMPARATORS present ==")
for g in ("Oahu_EGS", "Oahu_LSFO_CCGT", "Oahu_Puuloa", "Oahu_Waiau_Repower"):
    ok(f"{g} in gen_build_costs", cost(GBC, g, "2030", 2) is not None or cost(GBC, g, "2027", 2) is not None)

print("\n" + ("=" * 60))
print("ALL CLAIMS VERIFIED" if not FAILS else f"{len(FAILS)} FAILED: " + ", ".join(FAILS))
sys.exit(1 if FAILS else 0)

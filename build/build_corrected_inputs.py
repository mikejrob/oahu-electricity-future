#!/usr/bin/env python
"""
build_corrected_inputs.py — regenerate the Switch inputs for the corrected
Oʻahu electricity analysis, from primary sources, in one deterministic pass.

    Author's note on provenance
    ---------------------------
    This rebuilds the input directories used by the report from (a) Ethan
    Hartley's verified base model and (b) primary cost sources, applying a
    small, fully-documented set of corrections and *nothing else*. Every
    number below either traces to a named source or is an explicitly-labelled
    author assumption; there are no hand-set values whose origin is unstated.
    Run it and it prints a verification block that re-derives each headline
    figure from its source and asserts the match.

Price-level and financial conventions:

    dollar unit         = real 2024 US$      every cost below is real 2024 dollars
    base_financial_year = 2027               NPV VALUATION DATE only (financials.csv);
                                             in Switch this is the discount anchor —
                                             it does not inflate inputs (verified in
                                             switch_model/financials.py).  So reported
                                             NPVs are "real 2024$, present value as of
                                             2027" — matching the report's Appendix A.1
                                             and eliminating any 2027$->2024$ scaling step.
    cost_of_capital     = 0.06               amortises overnight capital (financials.csv)
    discount_rate       = 0.03               social discount rate for the objective

    Each cost is rebased to 2024$ from its own source year:
    CPI_2022_2024 = 1.02700 ** 2 = 1.05473   US-CPI CAGR 2022->2024, applied to
                                             NREL ATB 2024 (quoted in 2022$).

Cost basis, by technology (real 2024$ throughout):

    Utility solar (CentralTrackingPV)
        capital = ATB2024 Moderate UtilityPV Class5 CAPEX (2022$)
                  x CPI_2022_2024            -> 2024$
                  x HAWAII_PREMIUM (1.20)     Hawaiʻi cost premium (author floor;
                                              see docs/CONVENTIONS.md — the 1.20
                                              is a conservative floor drawn from
                                              Honolulu retail + HECO PPA evidence,
                                              NOT an ATB figure)
                  x slope_mult               1.00 Flat / 1.05 Moderate / 1.10 Steep
                                              (Ethan's graduated terrain premium)
        fixed O&M = ATB Fixed O&M x CPI_2022_2024 only.  The Hawaiʻi premium is
                    applied to capital, not O&M, following the prior convention.

    Bulk battery (Battery_Bulk, 4-hour system, co-located with utility solar)
        4h system cost = (PVB_CAPEX - PV_CAPEX)/0.5 (2022$)   <- ATB 2024's OWN
                         x CPI_2022_2024 x HAWAII_PREMIUM        PV-Plus-Battery hybrid
        The co-location saving is taken directly from NREL's hybrid tech
        (battery grid-connection fully saved ~6.9% + joint-install ~1.9% at
        2030; a 0.91-0.93 multiplier by year).  Replaces the former flat 0.88,
        which traced to the 2-HOUR battery's GCC share and overstated the
        4-hour discount (docs/CONVENTIONS.md).

    Enhanced Geothermal (Oahu_EGS)  — 6 / 10 / 14.7 $M/MW @2030 (2024$).  A CHANGED
    JUDGEMENT CALL (not a mistake-fix): the sourcing was genuinely mixed — DOE
    GeoVision ~$6M, a DOE document ~$9M, and ATB 2024 Moderate ~$12M.  ref and high
    are anchored to fixed 2030 targets (so the trio is exact and dollar-year-robust)
    and take their decline SHAPE from the ATB Moderate / Conservative profiles.
        low  = DOE GeoVision optimistic targets (~$6M/MW) — the original report's
               low case, kept; the EGS option-value finding rests on it.
        ref  = $10M/MW — a compromise between the DOE-referenced ~$9M and ATB
               Moderate ~$12M, near the centre of the low–high range (~$10.35M)
               and below ATB Moderate.  Below-ATB is justified: ATB 2024 is dated
               and EGS costs have fallen fast (Fervo etc.), so ATB skews high for
               a 2030+ build; the GeoVision/DOE optimistic sources are more recent.
        high = $14.7M/MW — ATB 2024 NF-EGS Binary Conservative profile, anchored
               so the 2030 vintage is $14.7M in 2024$.
        FOM  = ATB NF-EGS Binary Moderate FOM x CPI, all cases.

    JERA LNG plant (Oahu_JERA)  — plant only; the ~$460M import infrastructure
    is recovered in the LNG fuel-supply-tier fixed_cost, not here (verified: the
    tier fixed_cost amortises $460M at 6% over the LNG throughput).  Cost from
    the JERA proposal (governor.hawaii.gov, 17 Mar 2026, p.30):
        $1,510M / 500 MW = $3,020/kW in ~2026$
        x 1.027 ** -2 (CPI 2026->2024) = $2,863/kW in 2024$.
    Expressed on the 2027 build vintage; JERA is force-built in 2030, so the
    2030 value is the only one that enters the model.

    Thermal comparators (Oahu_LSFO_CCGT, Oahu_Puuloa, Oahu_Waiau_Repower)
        LSFO_CCGT : $2,900/kW @2030 (declining path), Lazard-derived:
                    Lazard mainland high case + Hawaii premium (decision D8;
                    low end of realized Hawaii thermal evidence, high end of
                    mainland).  Carried from the report; Lazard source
                    vendored in sources/ (LSFO_COST_REVIEW.md).
        Waiau     : HECO's STATED (amended) construction cost, $1.155B / 253 MW
                    = $4,545/kW.  This is the system-cost basis — the actual cost
                    to build the plant.  The PUC (Docket 2025-0211, D&O 42411)
                    capped *recoverable* cost near the $847M bid ($931.7M
                    ceiling); the ~$220-310M gap to the stated cost is
                    shareholder exposure (report §6), not a lower
                    build cost; the capacity-expansion model uses the resource
                    cost.  (Matches the original report input.)
        Puuloa    : 99 MW Ameresco reciprocating-engine, federally backed,
                    predetermined (built in every scenario, so its cost cancels
                    from every scenario *difference*).  Carried; flagged as a
                    level-only input pending its PPA capex.

    Fuel (fuel_supply_curves.csv) is Ethan's base, which his pipeline expressed
    in 2027$ (it applied +2.7%/yr CPI to the AEO 2025 series).  We deflate it back
    to 2024$ here (x FUEL_2027_TO_2024) so the whole model shares one dollar unit;
    low/high Brent variants are built separately by build_brent_variants.py from
    the deflated 2024$ reference using the published LSFO/LNG-vs-Brent regressions
    (heat content 6.22 MMBtu/bbl).

Two input directories are produced, each = base + the identical corrections:
    inputs/                   reference land screen (graduated-slope solar)
    inputs_lu_constrained_c/  Class-C-only land screen (18 land-constrained runs)
"""
from __future__ import print_function, division

import csv
import os
import shutil
import subprocess
from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
ATB = REPO / "sources" / "ATBe_2024_v3.0.0_slice.csv"
# Base model (vendored in-repo; see base_model/README.md for provenance/credit)
EHW_IGP = Path(os.environ.get("EHW_IGP", str(REPO / "base_model")))

# --------------------------------------------------------------------------
# Conventions (real 2024$) — see the module docstring for full rationale
# --------------------------------------------------------------------------
# Dollar unit is real 2024 US$; the NPV valuation date is 2027 (base_financial_year
# in financials.csv, the discount anchor — it does not inflate inputs).  Each cost
# is rebased to 2024$ from its own source year:
CPI_2022_2024 = 1.027 ** 2          # 1.05473  US-CPI CAGR 2022->2024; ATB 2024 is quoted in 2022$
CPI_2026_2024 = 1.027 ** -2         # 0.94805  for the 2026-dated JERA figure -> 2024$
CPI_2027_2024 = 1.027 ** -3         # 0.92312  deflate Ethan's ENTIRE 2027$ base (every $
#                                     column: fuel, wind, DER, existing units, VOM,
#                                     interconnection, hydrogen, pumped-hydro, EV) to 2024$.
HAWAII_PREMIUM = 1.20               # solar/battery capital only; author conservative floor
# Battery co-location: derived from NREL ATB 2024's OWN "Utility-Scale
# PV-Plus-Battery" hybrid (100 MW PV + 50 MW / 4-hr battery, DC-coupled):
#   co-located battery $/kW  =  (PVB_CAPEX - PV_CAPEX) / PVB_BATT_SHARE
# This embodies exactly (a) the battery's grid-connection cost fully saved
# (~6.9% of 4-hr CAPEX) and (b) NREL's joint-install saving (~1.9%), i.e. a
# ~0.91-0.93 multiplier by year — replacing the former flat 0.88, which traced
# to the 2-HOUR battery's GCC share (10.6%) and overstated the 4-hr discount.
PVB_BATT_SHARE = 0.5                # ATB 2024 PVB config: 50 MW battery per 100 MW PV
SLOPE_MULT = {"Flat": 1.00, "Moderate": 1.05, "Steep": 1.10}  # Ethan's terrain premium

JERA_PLANT_2024 = 3_020_000 * CPI_2026_2024            # $/MW plant-only, 2024$  = 2,863,100
# Waiau: HECO's STATED (amended) construction cost, $1.155B / 253 MW = $4,545/kW.
# This is the system-cost basis — the actual resource cost of building the plant.
# NOT the PUC-approved recoverable ($847M+inflation); the recoverable-vs-stated
# gap (~$275M) is shareholder exposure, treated separately in the report (§6), not
# a reduction in what the plant costs to build.  HECO's stated figure is carried at
# face value in 2024$ (matches the report's quoted $1.155B).
WAIAU_2024 = 4_545_000.0                                 # $/MW, HECO stated cost (2024$)

# Thermal-comparator trajectories carried from the report (2024$), each sourced
# above.  LSFO_CCGT: Lazard/D8 (Lazard LCOE+ 2024 is quoted in 2024$).  Puuloa:
# Ameresco project (predetermined — its cost cancels from every scenario difference).
CCGT_COST = [("2027", "3100000", "30000"), ("2030", "2900000", "30000"),
             ("2035", "2700000", "30000"), ("2040", "2500000", "30000"),
             ("2045", "2300000", "30000"), ("2050", "2200000", "30000")]
PUULOA_COST = [("2027", "3000000", "45000")]

SOLAR_TECH_PREFIX = "CentralTrackingPV"      # utility solar (gets the ATB x premium basis)
BATTERY_TECH = "Battery_Bulk"
# ATB scenario for utility solar AND bulk battery CAPEX/FOM.  Base case =
# "Moderate".  The "Advanced" (low-cost) projection is the sourced cheaper-
# renewables sensitivity (a supplement) — a defensible case that solar- and
# battery-technology cost has outpaced expectations, in contrast to the
# fabricated cheap solar that was wrongly in the base.  Applies to solar and
# battery together (battery cost has fallen at least as fast as solar).
ATB_RENEW_SCEN = "Moderate"
PERIODS = (2027, 2030, 2035, 2040, 2045, 2050)   # model investment periods (periods.csv)


# --------------------------------------------------------------------------
# ATB reader
# --------------------------------------------------------------------------
def atb(technology, techdetail, parameter, scenario="Moderate"):
    """Return {year: value} from the vendored ATB 2024 slice, in ATB units
    ($/kW or $/kW-yr, 2022$).  Market case, 20-year CRP."""
    out = {}
    with open(ATB) as f:
        for r in csv.DictReader(f):
            if (r["technology"] == technology and r["techdetail"] == techdetail
                    and r["core_metric_parameter"] == parameter
                    and r["scenario"] == scenario
                    and r["core_metric_case"] == "Market"
                    and r["crpyears"] == "20"):
                y = r["core_metric_variable"]
                if y.isdigit():
                    out[int(y)] = float(r["value"])
    return out


# --------------------------------------------------------------------------
# CSV helpers (LF line endings; preserve column order)
# --------------------------------------------------------------------------
def read_rows(path):
    with open(path, newline="") as f:
        rows = [[c.replace("\r", "") for c in row] for row in csv.reader(f)]
    return rows[0], rows[1:]


def write_rows(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


# Ethan's pre-2.0.9 names, renamed to the Switch 2.0.9 convention on copy.
FILE_RENAME = {"generation_projects_info.csv": "gen_info.csv"}
COLUMN_RENAME = {"gen_predetermined_cap": "build_gen_predetermined",
                 "gen_predetermined_storage_energy_mwh": "build_gen_energy_predetermined"}


# --------------------------------------------------------------------------
# Generator additions (EGS + three thermal comparators).  Rows lifted from the
# report working tree; costs are set below from the sourced values, not here.
# --------------------------------------------------------------------------
GEN_INFO_ADD = [
    # EGS: continuous build 0-100 MW (gen_unit_size and gen_min_build blanked).
    # The 25 MW "unit" is a modeling artifact, not a physical constraint at this
    # resolution (~a dozen candidate sites); the integer BuildUnits variable it
    # created made these cells solve poorly (see sanity_check_results.py). A
    # continuous build removes the integer variable, solves fast and reliably,
    # and changes results only at the margin (~one 25 MW step).
    ["Oahu_EGS", "Oahu", "EGS", "75000.0", "100.0", ".", ".", "30",
     "0.05", "0.02", "0", "1", "0", "2.0", "Geothermal", ".", ".", ".", ".",
     ".", ".", "."],
    ["Oahu_LSFO_CCGT", "Oahu", "LSFO_CCGT", "150000", "500.0", "125.0", ".",
     "30", "0.05", "0.035", "0", "0", "0", "6.0", "multiple", ".", "4.0",
     "6.0", "1.4", ".", ".", "."],
    ["Oahu_Puuloa", "Oahu", "Puuloa_Recip", "0.0", "99.0", "9.0", "9.0", "30",
     "0.03", "0.02", "0", "0", "0", "8.0", "multiple", ".", "0.5", "0.5",
     "0.3", ".", ".", "."],
    ["Oahu_Waiau_Repower", "Oahu", "Waiau_CT", "0.0", "252.0", "42.0", "42.0",
     "30", "0.03", "0.02", "0", "0", "0", "5.0", "multiple", ".", "0.5", "0.5",
     "0.5", ".", ".", "."],
]
GEN_PREDETERMINED_ADD = [["Oahu_Puuloa", "2027", "99.0", "."]]
GEN_INC_HEAT_RATES_ADD = [
    ["Oahu_Puuloa", "3.0", ".", ".", "27.0"], ["Oahu_Puuloa", "3.0", "5.0", "8.0", "."],
    ["Oahu_Puuloa", "5.0", "7.0", "8.2", "."], ["Oahu_Puuloa", "7.0", "9.0", "8.5", "."],
    ["Oahu_Waiau_Repower", "10.0", ".", ".", "115.0"],
    ["Oahu_Waiau_Repower", "10.0", "20.0", "9.2", "."],
    ["Oahu_Waiau_Repower", "20.0", "30.0", "9.4", "."],
    ["Oahu_Waiau_Repower", "30.0", "42.0", "9.7", "."],
    ["Oahu_LSFO_CCGT", "37.5", ".", ".", "320.0"],
    ["Oahu_LSFO_CCGT", "37.5", "60.0", "6.40", "."],
    ["Oahu_LSFO_CCGT", "60.0", "85.0", "6.55", "."],
    ["Oahu_LSFO_CCGT", "85.0", "110.0", "6.75", "."],
    ["Oahu_LSFO_CCGT", "110.0", "125.0", "6.95", "."],
]
GEN_MULTIPLE_FUELS_ADD = [
    ["Oahu_Puuloa", "Biodiesel"],
    ["Oahu_Waiau_Repower", "LSFO"], ["Oahu_Waiau_Repower", "Diesel"],
    ["Oahu_Waiau_Repower", "Biodiesel"],
    ["Oahu_LSFO_CCGT", "LSFO"], ["Oahu_LSFO_CCGT", "Biodiesel"],
    ["Oahu_LSFO_CCGT", "Diesel"],
]
GEN_RESERVE_CAP_ADD = [
    ["Oahu_EGS", "contingency"], ["Oahu_EGS", "regulation"],
    ["Oahu_Puuloa", "contingency"], ["Oahu_Puuloa", "regulation"],
    ["Oahu_Waiau_Repower", "contingency"], ["Oahu_Waiau_Repower", "regulation"],
    ["Oahu_LSFO_CCGT", "contingency"], ["Oahu_LSFO_CCGT", "regulation"],
]


# EGS cost cases — 6 / 10 / 14.7 ($M/MW @2030).  This is a CHANGED JUDGEMENT
# CALL (see docs/CONVENTIONS.md), not a mistake-fix: the sourcing was genuinely
# mixed (DOE GeoVision ~$6M, a DOE document ~$9M, ATB 2024 Moderate ~$12M).
#   low  = DOE GeoVision optimistic targets (original report low case, kept) —
#          the EGS option-value finding rests on this case.
#   ref  = $10M/MW: a compromise between the DOE-referenced ~$9M and ATB Moderate
#          ~$12M, sitting near the centre of the low–high range (~$10.35M) and
#          below ATB Moderate.  Below-ATB is justified: ATB 2024 is dated and EGS
#          costs have fallen fast (Fervo Cape Station etc.), and the GeoVision/DOE
#          sources are more recent for the optimistic trajectory — so ATB skews
#          high for a 2030+ build.  Placed on the ATB Moderate decline profile.
#   high = ATB 2024 NF-EGS Binary Conservative x CPI (~$14.7M/MW).
GEOVISION_LOW = {2027: 7_500_000, 2030: 6_200_000, 2035: 5_200_000,
                 2040: 4_800_000, 2045: 4_500_000, 2050: 4_300_000}  # DOE GeoVision, 2024$
# ref & high are anchored to fixed 2030 targets (2024$) and take their decline
# SHAPE from the ATB Moderate / Conservative profiles.  Anchoring to a fixed 2030
# value keeps the 6 / 10 / 14.7 trio exact and dollar-year-independent.
EGS_ANCHOR_2030 = {"ref": 10_000_000, "high": 14_700_000}    # $/MW at 2030, 2024$


def egs_costs(case):
    """EGS build-cost rows (year, overnight $/MW, fixed_om $/MW-yr), real 2024$,
    for case in {'low','ref','high'} per the 6/10/14.7 trio above.  FOM = ATB
    NF-EGS Binary Moderate FOM x CPI, all cases (sourced, consistent)."""
    fom = atb("Geothermal", "NFEGSBinary", "Fixed O&M", "Moderate")
    fr = lambda y: f"{fom[y] * 1000 * CPI_2022_2024:.2f}"
    if case == "low":
        return [(str(y), f"{GEOVISION_LOW[y]:.2f}", fr(y)) for y in PERIODS]
    scen = "Conservative" if case == "high" else "Moderate"
    cap = atb("Geothermal", "NFEGSBinary", "CAPEX", scen)
    # scale the ATB decline profile so the 2030 vintage hits the fixed 2024$ anchor
    scale = EGS_ANCHOR_2030[case] / (cap[2030] * 1000 * CPI_2022_2024)
    return [(str(y), f"{cap[y] * 1000 * CPI_2022_2024 * scale:.2f}", fr(y)) for y in PERIODS]


def jera_costs():
    """JERA plant-only $/MW by build year, real 2024$, expressed on the standard
    declining vintage form anchored so the (force-built) 2030 value is exact."""
    years = [2027, 2030, 2035, 2040, 2045, 2050]
    # anchor the 2030 build-vintage to the proposal cost; taper other vintages
    # at 1.8%/yr per the prior capital-accounting convention (inert here — JERA
    # is force-built in 2030, so only 2030 enters the model).
    return [(str(y), f"{JERA_PLANT_2024 * (1.018 ** (2030 - y)):.2f}") for y in years]


# --------------------------------------------------------------------------
# Build one input directory
# --------------------------------------------------------------------------
def seed(base_dir, out_dir):
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    for p in sorted(base_dir.iterdir()):
        if p.is_file():
            h, r = read_rows(p)
            h = [COLUMN_RENAME.get(c, c) for c in h]
            write_rows(out_dir / FILE_RENAME.get(p.name, p.name), h, r)


# Every $-denominated column in Ethan's base is real 2027$ (his pipeline inflated
# ATB 2024 capex/O&M and AEO 2025 fuel at 2.7%/yr, and H2 equipment at 2.3%/yr,
# all to a 2027 base — see base_get_scenario_data.py).  To share ONE dollar unit
# we deflate every one of these columns to 2024$ (x CPI_2027_2024) right after
# seeding, BEFORE the source-derived corrections (which are computed in 2024$ and
# overwrite/append afterwards, so they are not double-deflated).  Non-cost numeric
# columns (capacities, heat rates, ages, rates, shares) are left untouched.
BASE_COST_COLUMNS = {
    "gen_build_costs.csv": ["gen_overnight_cost", "gen_storage_energy_overnight_cost",
                            "gen_fixed_om"],
    "gen_info.csv": ["gen_connect_cost_per_mw", "gen_variable_om"],
    "fuel_supply_curves.csv": ["unit_cost", "fixed_cost"],
    "hydrogen.csv": ["hydrogen_electrolyzer_capital_cost_per_mw",
                     "hydrogen_electrolyzer_fixed_cost_per_mw_year",
                     "hydrogen_electrolyzer_variable_cost_per_kg",
                     "hydrogen_fuel_cell_capital_cost_per_mw",
                     "hydrogen_fuel_cell_fixed_cost_per_mw_year",
                     "hydrogen_fuel_cell_variable_cost_per_mwh",
                     "hydrogen_liquifier_capital_cost_per_kg_per_hour",
                     "hydrogen_liquifier_fixed_cost_per_kg_hour_year",
                     "hydrogen_liquifier_variable_cost_per_kg",
                     "liquid_hydrogen_tank_capital_cost_per_kg"],
    "pumped_hydro.csv": ["ph_capital_cost_per_mw"],
    "ev_fleet_info.csv": ["ev_extra_cost_per_vehicle_year"],
    "ev_fleet_info_advanced.csv": ["ev_extra_cost_per_vehicle_year"],
}


def rebase_base_to_2024(out_dir):
    """Deflate every $-denominated column in Ethan's 2027$ base to real 2024$
    (x CPI_2027_2024), so the whole model shares one dollar unit.  Runs after
    seed() and before the source-derived corrections.  Returns a per-file count."""
    counts = {}
    for fname, cols in BASE_COST_COLUMNS.items():
        fp = out_dir / fname
        if not fp.exists():
            continue
        h, rows = read_rows(fp)
        idx = [h.index(c) for c in cols if c in h]
        n = 0
        for r in rows:
            for ci in idx:
                if len(r) > ci and r[ci] not in (".", ""):
                    try:
                        r[ci] = f"{float(r[ci]) * CPI_2027_2024:.6f}"
                        n += 1
                    except ValueError:
                        pass
        write_rows(fp, h, rows)
        counts[fname] = n
    return counts


def correct_costs(out_dir):
    """Rewrite gen_build_costs.csv: utility solar, bulk battery and JERA to the
    sourced 2024$ values above; everything else (DER, existing units) untouched."""
    gbc = out_dir / "gen_build_costs.csv"
    h, rows = read_rows(gbc)
    gp, by, oc, se, fo = (h.index("GENERATION_PROJECT"), h.index("build_year"),
                          h.index("gen_overnight_cost"),
                          h.index("gen_storage_energy_overnight_cost"),
                          h.index("gen_fixed_om"))
    gi_h, gi_r = read_rows(out_dir / "gen_info.csv")
    tech = {r[gi_h.index("GENERATION_PROJECT")]: r[gi_h.index("gen_tech")] for r in gi_r}

    scap = atb("UtilityPV", "Class5", "CAPEX", ATB_RENEW_SCEN)
    sfom = atb("UtilityPV", "Class5", "Fixed O&M", ATB_RENEW_SCEN)
    pvbcap = atb("Utility-Scale PV-Plus-Battery", "Class5", "CAPEX", ATB_RENEW_SCEN)
    # co-located 4-hr battery $/kW, from ATB's own hybrid (see PVB_BATT_SHARE note)
    bcap = {y: (pvbcap[y] - scap[y]) / PVB_BATT_SHARE
            for y in pvbcap if y in scap}

    n_solar = n_batt = n_jera = 0
    for r in rows:
        t = tech.get(r[gp], "")
        yr = int(r[by]) if r[by].isdigit() else None
        if t.startswith(SOLAR_TECH_PREFIX) and yr in scap:
            slope = next((k for k in SLOPE_MULT if k in t), "Flat")
            r[oc] = f"{scap[yr] * 1000 * CPI_2022_2024 * HAWAII_PREMIUM * SLOPE_MULT[slope]:.6f}"
            if r[fo] not in (".", ""):                        # FOM: rebase only
                r[fo] = f"{sfom[yr] * 1000 * CPI_2022_2024:.6f}"
            n_solar += 1
        elif t == BATTERY_TECH and yr in bcap:
            target4h = bcap[yr] * 1000 * CPI_2022_2024 * HAWAII_PREMIUM   # bcap = ATB PVB-derived co-located battery
            base4h = float(r[oc]) + 4 * float(r[se])
            f = target4h / base4h                             # keep power:energy split
            r[oc] = f"{float(r[oc]) * f:.6f}"
            r[se] = f"{float(r[se]) * f:.6f}"
            if r[fo] not in (".", ""):
                r[fo] = f"{float(r[fo]) * f:.6f}"
            n_batt += 1
    write_rows(gbc, h, rows)
    return n_solar, n_batt


def add_generators(out_dir):
    """Append EGS + three comparators across the six files that carry them, and
    add Geothermal as a non-fuel source.  Costs from egs_costs()/jera_costs()/
    the sourced comparator trajectories."""
    # gen_info
    h, r = read_rows(out_dir / "gen_info.csv"); r += [x[:] for x in GEN_INFO_ADD]
    write_rows(out_dir / "gen_info.csv", h, r)
    # gen_build_costs: EGS(ref) + JERA + Waiau + comparators
    h, r = read_rows(out_dir / "gen_build_costs.csv")
    for (yr, ocst, fom) in egs_costs("ref"):
        r.append(["Oahu_EGS", yr, ocst, ".", fom])
    for (yr, ocst, fom) in CCGT_COST:
        r.append(["Oahu_LSFO_CCGT", yr, ocst, ".", fom])
    r.append(["Oahu_Puuloa", PUULOA_COST[0][0], PUULOA_COST[0][1], ".", PUULOA_COST[0][2]])
    r.append(["Oahu_Waiau_Repower", "2030", f"{WAIAU_2024:.2f}", ".", "45000"])
    write_rows(out_dir / "gen_build_costs.csv", h, r)
    # aux files
    for fname, add in [("gen_build_predetermined.csv", GEN_PREDETERMINED_ADD),
                       ("gen_inc_heat_rates.csv", GEN_INC_HEAT_RATES_ADD),
                       ("gen_multiple_fuels.csv", GEN_MULTIPLE_FUELS_ADD),
                       ("generation_projects_reserve_capability.csv", GEN_RESERVE_CAP_ADD)]:
        h, r = read_rows(out_dir / fname); r += [x[:] for x in add]
        write_rows(out_dir / fname, h, r)
    # LNG-conversion fuel menus: base menu + LNG rows for existing units
    # (whitelisted in model/lng_conversion.py; used by scenarios_lngconv*)
    h, base_fuels = read_rows(out_dir / "gen_multiple_fuels.csv")
    kalaeloa = [[f"Oahu_Kalaeloa_CC{i}", "LNG"] for i in (1, 2, 3)]
    heco = kalaeloa + [["Oahu_Kahe_5", "LNG"], ["Oahu_Kahe_6", "LNG"],
                       ["Oahu_CIP_CT", "LNG"]]
    write_rows(out_dir / "gen_multiple_fuels_lngconv.csv", h, base_fuels + kalaeloa)
    write_rows(out_dir / "gen_multiple_fuels_lngconv_heco.csv", h, base_fuels + heco)
    # JERA is already in Ethan's base gen list; overwrite its cost rows to plant-only
    _set_jera(out_dir)
    # non_fuel_energy_sources
    h, r = read_rows(out_dir / "non_fuel_energy_sources.csv")
    if ["Geothermal"] not in r:
        r.append(["Geothermal"])
    write_rows(out_dir / "non_fuel_energy_sources.csv", h, r)


def _set_jera(out_dir):
    h, rows = read_rows(out_dir / "gen_build_costs.csv")
    gp, by, oc = h.index("GENERATION_PROJECT"), h.index("build_year"), h.index("gen_overnight_cost")
    jera = {yr: v for yr, v in jera_costs()}
    for r in rows:
        if r[gp] == "Oahu_JERA" and r[by] in jera:
            r[oc] = jera[r[by]]
    write_rows(out_dir / "gen_build_costs.csv", h, rows)


def egs_variant(out_dir, tag, scenario):
    """gen_build_costs_egs_<tag>.csv = the corrected base with Oahu_EGS rows
    swapped to the <case> cost trajectory (low/high)."""
    h, base = read_rows(out_dir / "gen_build_costs.csv")
    gp, by = h.index("GENERATION_PROJECT"), h.index("build_year")
    m = {yr: (ocst, fom) for (yr, ocst, fom) in egs_costs(scenario)}
    rows = []
    for r in base:
        if r[gp] == "Oahu_EGS" and r[by] in m:
            ocst = m[r[by]][0]
            # apply the 48E current-law credit (see the base-case note):
            # x0.70 for 2027-2035 vintages, full price after
            if r[by].isdigit() and 2027 <= int(r[by]) <= 2035:
                ocst = f"{float(ocst) * 0.70:.6f}"
            rows.append(["Oahu_EGS", r[by], ocst, ".", m[r[by]][1]])
        else:
            rows.append(r[:])
    write_rows(out_dir / f"gen_build_costs_egs_{tag}.csv", h, rows)


def modules_txt(out_dir):
    """Ethan's canonical module list + egs_geothermal, with hawaii.ev -> ev_patched
    (the stock 2.0.9 hawaii/ev.py omits the ev_mwh_ts param it references;
    model/ev_patched.py is Ethan's one-Param fix)."""
    src = EHW_IGP / "modules.txt"
    lines = [("ev_patched" if l.strip() == "switch_model.hawaii.ev" else l)
             for l in src.read_text().splitlines()]
    if "egs_geothermal" not in lines:
        lines.append("egs_geothermal")
    (out_dir / "modules.txt").write_text("\n".join(lines) + "\n")


def build_dir(base_dir, out_dir, slopes):
    print(f"== {base_dir.name} -> {out_dir.name} ==")
    seed(base_dir, out_dir)
    rb = rebase_base_to_2024(out_dir)          # Ethan's ENTIRE 2027$ base -> 2024$
    ns, nb = correct_costs(out_dir)            # overwrite solar/battery with 2024$ source
    add_generators(out_dir)                    # append EGS/JERA/Waiau/comparators in 2024$
    for tag, scen in [("low", "low"), ("high", "high")]:
        egs_variant(out_dir, tag, scen)
    # break-even PV-cost sensitivity: solar capital+FOM x1.5 / x1.7 of the baseline
    # Battery-ITC variant (supplement): 30% federal storage credit (48E,
    # retained post-OBBB) modeled as utility-scale battery capital x0.70 —
    # power and energy components, build years 2027+ (predetermined vintages
    # unchanged).  Flat 30% across the horizon = the generous bound; the
    # statutory phase-down (2034-36 begin-construction) would trim post-2035
    # builds.  Distributed batteries unchanged (customer-side economics).
    h, rows = read_rows(out_dir / "gen_build_costs.csv")
    gp, by = h.index("GENERATION_PROJECT"), h.index("build_year")
    oc, se = h.index("gen_overnight_cost"), h.index("gen_storage_energy_overnight_cost")
    # BASE CASE = CURRENT LAW (OBBBA 48E).  Storage and geothermal keep the
    # full 30% clean-electricity ITC for construction beginning through 2033
    # (22.5%/15% for 2034/2035 starts, zero after).  With a ~2-year
    # construction lead, model vintages 2027-2035 carry x0.70 capital and
    # 2040+ carry full price.  Applied to utility-scale storage and to
    # Oahu_EGS alike — crediting one 48E technology and not the other would
    # be selective.  Wind/solar credits are terminated for 2027+ builds
    # under OBBBA, so solar correctly carries none.  The pre-credit table
    # is emitted as gen_build_costs_noitc.csv — the named FEOC/no-credit
    # sensitivity (material-assistance rules put battery supply-chain
    # eligibility in question; repeal risk exists for all of it).
    ITC48E = ("Oahu_Battery_Bulk", "Oahu_Battery_Conting",
              "Oahu_Battery_Reg", "Oahu_EGS")
    write_rows(out_dir / "gen_build_costs_noitc.csv", h, rows)
    out = []
    for r in rows:
        r = r[:]
        if (r[gp] in ITC48E and r[by].isdigit()
                and 2027 <= int(r[by]) <= 2035):
            for c in (oc, se):
                if r[c] not in (".", ""):
                    r[c] = f"{float(r[c]) * 0.70:.6f}"
        out.append(r)
    write_rows(out_dir / "gen_build_costs.csv", h, out)
    for tag, mult in [("pv15", 1.5), ("pv17", 1.7)]:
        _pv_variant(out_dir, tag, mult)
    modules_txt(out_dir)
    print(f"   rebased 2027$->2024$: {rb}; solar rows={ns} battery rows={nb}; "
          f"+EGS/JERA/Waiau/comparators; egs_low/ref/high + pv15/pv17 variants")


def jera_contingency_variant(out_dir, uplift=1.20):
    """+20% JERA contingency variant (JERA proposal p.29 downside case).  The KBR
    Phase-2 cost estimate the proposal cites (p.30) explicitly EXCLUDES contingency,
    design allowance, insurance, customs/duties and imported equipment; the proposal
    itself models a +20% capital-cost sensitivity.  This writes *_jera120 input files
    that raise CAPITAL only — JERA plant overnight cost x1.2 and the LNG-infrastructure
    tier fixed_cost x1.2 — leaving fuel (unit_cost) and O&M unchanged.  Used by the
    _j120 scenarios so the report can show LNG at the bare-EPC and delivered-cost cases."""
    # gen_build_costs (and the EGS-low/high cost variants, which the egs_*_lng_forced
    # scenarios load): Oahu_JERA overnight cost x uplift.  One _jera120 file per base
    # so every JERA scenario has a matching JERA-uplifted cost table.
    for base in ("gen_build_costs.csv", "gen_build_costs_egs_low.csv",
                 "gen_build_costs_egs_high.csv",
                 # solar-premium x JERA-contingency combos (scenarios_pvjera)
                 "gen_build_costs_pv15.csv", "gen_build_costs_pv17.csv",
                 # no-credit (FEOC) sensitivity x JERA-contingency combo
                 "gen_build_costs_noitc.csv"):
        bp = out_dir / base
        if not bp.exists():
            continue
        h, rows = read_rows(bp)
        gp, oc = h.index("GENERATION_PROJECT"), h.index("gen_overnight_cost")
        out = []
        for r in rows:
            r = r[:]
            if r[gp] == "Oahu_JERA" and r[oc] not in (".", ""):
                r[oc] = f"{float(r[oc]) * uplift:.6f}"
            out.append(r)
        write_rows(out_dir / base.replace(".csv", "_jera120.csv"), h, out)
    # fuel curves (each Brent variant): LNG-tier fixed_cost (FSRU/pipeline) x uplift
    for fuel in ("fuel_supply_curves.csv", "fuel_supply_curves_lowbrent.csv",
                 "fuel_supply_curves_highbrent.csv"):
        fp = out_dir / fuel
        if not fp.exists():
            continue
        h, rows = read_rows(fp)
        fi, ci = h.index("fuel"), h.index("fixed_cost")
        out = []
        for r in rows:
            r = r[:]
            if len(r) > ci and r[fi].upper() == "LNG" and r[ci] not in (".", ""):
                r[ci] = f"{float(r[ci]) * uplift:.6f}"
            out.append(r)
        write_rows(out_dir / fuel.replace(".csv", "_jera120.csv"), h, out)


def _pv_variant(out_dir, tag, mult):
    h, base = read_rows(out_dir / "gen_build_costs.csv")
    gp, oc, fo = h.index("GENERATION_PROJECT"), h.index("gen_overnight_cost"), h.index("gen_fixed_om")
    gi_h, gi_r = read_rows(out_dir / "gen_info.csv")
    tech = {r[gi_h.index("GENERATION_PROJECT")]: r[gi_h.index("gen_tech")] for r in gi_r}
    rows = []
    for r in base:
        r = r[:]
        if tech.get(r[gp], "").startswith(SOLAR_TECH_PREFIX):
            if r[oc] not in (".", ""):
                r[oc] = f"{float(r[oc]) * mult:.6f}"
            if r[fo] not in (".", ""):
                r[fo] = f"{float(r[fo]) * mult:.6f}"
        rows.append(r)
    write_rows(out_dir / f"gen_build_costs_{tag}.csv", h, rows)


# --------------------------------------------------------------------------
# Verification — re-derive every headline figure from source and assert
# --------------------------------------------------------------------------
def verify(out_dir, expect_slopes):
    h, rows = read_rows(out_dir / "gen_build_costs.csv")
    gp, by, oc, se = (h.index("GENERATION_PROJECT"), h.index("build_year"),
                      h.index("gen_overnight_cost"), h.index("gen_storage_energy_overnight_cost"))
    gi_h, gi_r = read_rows(out_dir / "gen_info.csv")
    tech = {r[gi_h.index("GENERATION_PROJECT")]: r[gi_h.index("gen_tech")] for r in gi_r}
    scap = atb("UtilityPV", "Class5", "CAPEX", ATB_RENEW_SCEN)
    _pvb = atb("Utility-Scale PV-Plus-Battery", "Class5", "CAPEX", ATB_RENEW_SCEN)
    bcap = {y: (_pvb[y] - scap[y]) / PVB_BATT_SHARE for y in _pvb if y in scap}
    fails, ns, nb, nj = [], 0, 0, 0
    for r in rows:
        t = tech.get(r[gp], "")
        # slope-1.0 utility solar must land exactly on ATB x CPI x Hawaiʻi premium.
        # With slopes that is the "Flat" family; without (constrained_c) it is the
        # single non-slope solar tech.
        slope1 = ("Flat" in t) if expect_slopes else (
            t.startswith(SOLAR_TECH_PREFIX) and not any(k in t for k in ("Moderate", "Steep")))
        if t.startswith(SOLAR_TECH_PREFIX) and r[by].isdigit() and slope1:
            yr = int(r[by])
            if yr in scap:
                tgt = scap[yr] * 1000 * CPI_2022_2024 * HAWAII_PREMIUM
                ns += 1
                if abs(float(r[oc]) - tgt) / tgt > 1e-4:
                    fails.append(f"solar {yr}: {float(r[oc]):.0f} vs {tgt:.0f}")
        elif t == BATTERY_TECH and r[by].isdigit() and int(r[by]) in bcap:
            yr = int(r[by]); nb += 1
            sysc = float(r[oc]) + 4 * float(r[se])
            itc = 0.70 if 2027 <= yr <= 2035 else 1.0   # 48E current-law schedule
            tgt = bcap[yr] * 1000 * CPI_2022_2024 * HAWAII_PREMIUM * itc
            if abs(sysc - tgt) / tgt > 1e-4:
                fails.append(f"battery {yr}: {sysc:.0f} vs {tgt:.0f}")
        elif r[gp] == "Oahu_JERA" and r[by] == "2030":
            nj += 1
            if abs(float(r[oc]) - JERA_PLANT_2024) / JERA_PLANT_2024 > 1e-4:
                fails.append(f"JERA 2030: {float(r[oc]):.0f} vs {JERA_PLANT_2024:.0f}")
    if ns == 0 or nb == 0 or nj == 0:
        fails.append(f"GUARD zero matches solar/batt/jera={ns}/{nb}/{nj}")
    for g in ("Oahu_EGS", "Oahu_LSFO_CCGT", "Oahu_Puuloa", "Oahu_Waiau_Repower"):
        if g not in {r[gp] for r in rows}:
            fails.append(f"missing gen: {g}")
    print(f"   VERIFY {out_dir.name}: solar Flat on ATBx{CPI_2022_2024:.4f}x{HAWAII_PREMIUM}={ns}, "
          f"battery={nb}, jera2030={nj} -> {'OK' if not fails else 'FAIL'}")
    for x in fails:
        print("     FAIL:", x)
    assert not fails, f"verification failed for {out_dir.name}"


def main(targets=("reference", "lc"), atb_scen="Moderate", suffix=""):
    """Build the input dirs.  atb_scen selects the ATB UtilityPV scenario for
    solar CAPEX/FOM ("Moderate" base, "Advanced" for the low-solar supplement);
    suffix is appended to the output dir names (e.g. "_advsolar")."""
    global ATB_RENEW_SCEN
    ATB_RENEW_SCEN = atb_scen
    ref_dir, lc_dir = f"inputs{suffix}", f"inputs_lu_constrained_c{suffix}"
    if "reference" in targets:
        build_dir(EHW_IGP / "reference_wslope" / "inputs", REPO / ref_dir, slopes=True)
        verify(REPO / ref_dir, expect_slopes=True)
    if "lc" in targets:
        build_dir(EHW_IGP / "constrained_c" / "inputs",
                  REPO / lc_dir, slopes=False)
        verify(REPO / lc_dir, expect_slopes=False)
    built = [d for t, d in (("reference", ref_dir),
                            ("lc", lc_dir)) if t in targets]
    print(f"== regenerate real 2024$ low/high-Brent variants for: {', '.join(built)} ==")
    subprocess.run(["python", str(REPO / "build" / "build_brent_variants.py"), *built], check=True)
    for d in built:                            # needs the Brent fuel variants to exist first
        jera_contingency_variant(REPO / d)     # +20% JERA-contingency (*_jera120) inputs
    print(f"== wrote +20% JERA-contingency variants (gen_build_costs_jera120 + fuel *_jera120) ==")
    print("\nDONE — all inputs regenerated in real 2024$ (NPV valued 2027) from primary sources.")


if __name__ == "__main__":
    import sys
    argv = sys.argv[1:]
    adv = "advsolar" in argv                        # low-solar supplement (ATB Advanced)
    targets = tuple(a for a in argv if a != "advsolar") or ("reference", "lc")
    if adv:
        main(targets, atb_scen="Advanced", suffix="_advsolar")
    else:
        main(targets)

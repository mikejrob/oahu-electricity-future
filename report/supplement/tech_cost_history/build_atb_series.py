#!/usr/bin/env python
"""
Build the ATB-vintage projection series for utility-scale PV and 4-hour battery,
for fixed future target years 2030 and 2050, Moderate (mid) scenario, Market case.

INPUTS (all downloaded directly, see data/SOURCES in SOURCES.md):
  data/atbe_csv/ATBe_{2019..2023}.csv, ATBe_2024_v3.csv   -- OEDI data-lake structured CSVs
  data/cpi_u_annual.csv                                    -- BLS CPI-U annual avg (from FRED CPIAUCSL)

METRIC CHOICES (documented for reviewer):
  * PV:   CAPEX in $/kW.  2020-2024 are on an AC basis ($/kW_AC) and are directly
          comparable.  The 2019 ATB reported PV on a DC basis ($/kW_DC) and is therefore
          NOT unit-comparable; it is extracted but flagged and excluded from the headline PV series.
  * BATT: 4-hour utility-scale battery.  2021-2024 report a duration-resolved 4Hr number.
          2019-2020 report a single power-based battery CAPEX not split by duration and are
          excluded from the headline battery series (flagged).
          NOTE: 2019-2022 label the CAPEX parameter "CAPEX"; 2023-2024 report only "OCC"
          (overnight capital cost) for battery.  OCC excludes grid-interconnection and
          construction financing that CAPEX includes, so the 2022->2023 battery step mixes a
          real cost change with this definitional change.  We record BOTH the metric name used
          and, for PV where both exist (2023,2024), the CAPEX-vs-OCC gap, so the reviewer can judge.

DOLLAR YEARS (verified from each workbook's "Solar - Utility PV" sheet header, see SOURCES.md):
  ATB2019->2017$  ATB2020->2018$  ATB2021->2019$  ATB2022->2020$  ATB2023->2021$  ATB2024->2022$
All series are additionally deflated to a common REAL 2024$ using BLS CPI-U annual averages
(base year = CPI-U 2024 annual average = 313.698, computed from the FRED CPIAUCSL 2024 monthly
series and cross-checked to the published BLS CPI-U 2024 annual average ~313.689; see SOURCES.md).

OUTPUTS:
  data/atb_projection_series.csv          -- fixed target-year (2030,2050) points, all vintages
  data/atb_pv_trajectories_2024usd.csv    -- full PV CAPEX trajectory (2022-2050) per vintage
"""
import pandas as pd, os

HERE = os.path.dirname(os.path.abspath(__file__))
CSVDIR = os.path.join(HERE, "data", "atbe_csv")

# ATB vintage -> (file, dollar-year of that vintage)
VINTAGES = {
    2019: ("ATBe_2019.csv", 2017),
    2020: ("ATBe_2020.csv", 2018),
    2021: ("ATBe_2021.csv", 2019),
    2022: ("ATBe_2022.csv", 2020),
    2023: ("ATBe_2023.csv", 2021),
    2024: ("ATBe_2024_v3.csv", 2022),
}
# scenario label used for the "mid" case (2019 used "Mid", 2020+ "Moderate")
MID = {2019: "Mid", 2020: "Moderate", 2021: "Moderate", 2022: "Moderate",
       2023: "Moderate", 2024: "Moderate"}
# battery technology label
BTECH = {2019: "Battery", 2020: "Battery", 2021: "Utility-Scale Battery Storage",
         2022: "Utility-Scale Battery Storage", 2023: "Utility-Scale Battery Storage",
         2024: "Utility-Scale Battery Storage"}
# PV techdetail that carries CAPEX (class/resource-invariant; verified)
PVTD = {2019: "Daggett", 2020: "Daggett", 2021: "Class5", 2022: "Class5",
        2023: "Class5", 2024: "Class5"}

# CPI-U annual averages (BLS, via FRED CPIAUCSL monthly -> annual mean)
cpi = pd.read_csv(os.path.join(HERE, "data", "cpi_u_annual.csv")).set_index("year")["cpi_u"]
BASE = cpi.loc[2024]   # rebased 2022$ -> real 2024$ (common base year)

def val(df, tech, td, param, scen, case, yr):
    m = ((df["technology"] == tech) & (df["core_metric_parameter"] == param) &
         (df["scenario"] == scen) & (df["core_metric_case"] == case) &
         (df["core_metric_variable"] == yr))
    if td is not None:
        m &= (df["techdetail"] == td)
    v = df.loc[m, "value"].dropna().unique()
    return float(v[0]) if len(v) else None

rows = []
traj_rows = []   # full PV CAPEX trajectory (2022-2050) per vintage, for the fan figure
for vint, (fn, dolyr) in VINTAGES.items():
    df = pd.read_csv(os.path.join(CSVDIR, fn), low_memory=False)
    df["core_metric_variable"] = pd.to_numeric(df["core_metric_variable"], errors="coerce")
    defl = BASE / cpi.loc[dolyr]  # multiply native -> real 2024$
    for target in (2030, 2050):
        # --- PV: prefer CAPEX (all years have it); also record OCC where present ---
        pv_capex = val(df, "UtilityPV", PVTD[vint], "CAPEX", MID[vint], "Market", target)
        pv_occ   = val(df, "UtilityPV", PVTD[vint], "OCC",   MID[vint], "Market", target)
        pv_basis = "DC" if vint == 2019 else "AC"
        rows.append(dict(atb_vintage=vint, dollar_year=dolyr, technology="UtilityPV",
                         target_year=target, metric="CAPEX", pv_basis=pv_basis,
                         value_native=pv_capex,
                         value_2024usd=(pv_capex*defl if pv_capex is not None else None),
                         headline=(pv_capex is not None and vint >= 2020)))
        if pv_occ is not None:
            rows.append(dict(atb_vintage=vint, dollar_year=dolyr, technology="UtilityPV",
                             target_year=target, metric="OCC", pv_basis=pv_basis,
                             value_native=pv_occ, value_2024usd=pv_occ*defl, headline=False))
        # --- Battery 4Hr: CAPEX for 2021-2022, OCC for 2023-2024 ---
        bt = BTECH[vint]
        for param in ("CAPEX", "OCC"):
            bv = val(df, bt, "4Hr Battery Storage", param, MID[vint], "Market", target)
            if bv is not None:
                rows.append(dict(atb_vintage=vint, dollar_year=dolyr,
                                 technology="Battery_4hr", target_year=target,
                                 metric=param, pv_basis="",
                                 value_native=bv, value_2024usd=bv*defl,
                                 headline=(vint >= 2021)))
    # --- full PV CAPEX trajectory 2022-2050 (AC-basis vintages, i.e. 2020+) for the fan figure ---
    if vint >= 2020:
        for ty in range(2022, 2051):
            pv = val(df, "UtilityPV", PVTD[vint], "CAPEX", MID[vint], "Market", ty)
            if pv is not None:
                traj_rows.append(dict(atb_vintage=vint, tech="UtilityPV",
                                      target_year=ty, value_2024usd=pv*defl))

out = pd.DataFrame(rows).sort_values(["technology", "target_year", "atb_vintage", "metric"])
out.to_csv(os.path.join(HERE, "data", "atb_projection_series.csv"), index=False)
print(out.to_string(index=False))

traj = pd.DataFrame(traj_rows).sort_values(["atb_vintage", "target_year"])
traj.to_csv(os.path.join(HERE, "data", "atb_pv_trajectories_2024usd.csv"), index=False)
print("\nwrote atb_pv_trajectories_2024usd.csv rows:", len(traj))

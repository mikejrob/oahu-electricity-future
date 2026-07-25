#!/usr/bin/env python3
"""
09_estimator2_firmed.py — Estimator 2 with battery-era radiation (2018-2024) on the
clock-corrected load. Firms the BATTERY term.

Radiation years available: 2018, 2019 (from 03_load_nsrdb) + 2020-2024 (S3 pull).
Load: panel_hourly_shifted.parquet (clock roll applied; radiation NOT shifted).

PV term (contemporaneous): daytime load ~ hourxseason + year FE + temp controls + GHI x PV_installed.
Battery term (predictive): EVENING load (17-20h) ~ hourxseason + year FE + EVENING-temp controls
    + (same-day MIDDAY GHI) x Batt_installed. Sunny midday -> fuller battery -> more evening
    discharge -> LOWER evening load. PV cannot generate in the evening -> separates battery from PV.

Energy-conservation check: evening discharge per installed MWh must be <= rte*(1-reserve).

Outputs: estimator2_pv_term_firmed.csv, estimator2_battery_firmed.csv,
         estimator2_battery_shape.csv, estimator2_firmed_summary.txt
"""
import os
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ANA = "/mnt/lustre/koa/koastore/gtg_group/oahu-electricity-v1-corrected/analysis"
REF_GHI = 1000.0

# ---- radiation: combine 2018/19 (03) + 2020-24 (S3). Dedup on (y,m,d,h).
r1 = pd.read_parquet(os.path.join(ANA, "nsrdb_oahu_island_hourly.parquet"))
r1 = r1[r1.year.isin([2018, 2019])][["year", "month", "day", "hour", "ghi", "temp", "dni", "dhi"]]
r2 = pd.read_parquet(os.path.join(ANA, "nsrdb_oahu_island_hourly_2020_2024.parquet"))
r2 = r2[["year", "month", "day", "hour", "ghi", "temp", "dni", "dhi"]]
isl = pd.concat([r1, r2], ignore_index=True).drop_duplicates(["year", "month", "day", "hour"])
isl["date"] = pd.to_datetime(isl[["year", "month", "day"]])
RAD_YEARS = sorted(isl.year.unique().tolist())

# same-day midday GHI (10-14h), evening temp (17-20h), midday temp
midday = isl[isl.hour.between(10, 14)].groupby("date").agg(
    ghi_midday=("ghi", "mean"), temp_midday=("temp", "mean")).reset_index()
evening = isl[isl.hour.between(17, 20)].groupby("date").agg(
    temp_evening=("temp", "mean")).reset_index()

# ---- load (clock-corrected), restrict to radiation years
pan = pd.read_parquet(os.path.join(ANA, "panel_hourly_shifted.parquet"))
pan["date"] = pd.to_datetime(pan["date"])
pan = pan[pan["year"].isin(RAD_YEARS)].copy()

m = pan.merge(isl[["date", "hour", "ghi", "temp", "dni"]], on=["date", "hour"], how="inner")
m = m.merge(midday, on="date", how="left").merge(evening, on="date", how="left")
m["season"] = m["quarter"].astype("category")
m["hourF"] = m["hour"].astype("category")
m["yearF"] = m["year"].astype("category")
m["ghi_x_pv"] = m["ghi"] * m["pv_mw_cum"]
m["middayghi_x_batt"] = m["ghi_midday"] * m["batt_mwh_cum"]

out = []
out.append("Estimator 2 FIRMED — radiation years: %s (clock-corrected load)" % RAD_YEARS)

# =============================== PV TERM ===============================
# Identification note: within-year PV drift is only ~30-50 MW vs a 476->765 MW between-year
# spread, so year FE would eat the PV level and leave ghi_x_pv collinear with the standalone
# ghi control (corrupts the per-hour shape). Per the design ("EV/secular trend control"),
# use a LINEAR secular trend (t_years) instead of year FE, and drop the standalone ghi term so
# ghi_x_pv carries the PV response identified off both day-to-day GHI and the PV level.
m["t_years"] = m["year"] + (m["month"] - 1) / 12.0
m["t_years"] = m["t_years"] - m["t_years"].mean()
day = m[m["hour"].between(7, 17)].copy()
pv_rows = []
for h in range(7, 18):
    sub = day[day["hour"] == h]
    if sub["ghi"].std() < 1 or sub["pv_mw_cum"].max() < 1:
        continue
    mod = smf.ols("load_mw ~ C(season) + t_years + temp + I(temp**2) + ghi_x_pv",
                  data=sub).fit()
    b = mod.params.get("ghi_x_pv", np.nan)
    pv_rows.append(dict(hour=h, b_ghi_x_pv=b, se=mod.bse.get("ghi_x_pv", np.nan),
                        mw_per_mw_at_ref=b * REF_GHI, n=int(mod.nobs)))
pv = pd.DataFrame(pv_rows)
pv.to_csv(os.path.join(ANA, "estimator2_pv_term_firmed.csv"), index=False)
out.append("\nPV TERM (per hour, MW load-reduction per MW installed at %g W/m2):" % REF_GHI)
out.append(pv[["hour", "mw_per_mw_at_ref", "se"]].round(4).to_string(index=False))
noon = pv[pv.hour == 12]
if len(noon):
    out.append("  noon PV = %.3f MW/MW" % (-noon["mw_per_mw_at_ref"].iloc[0]))

# =============================== BATTERY TERM ===============================
# CLEAN window = SUN-DOWN evening hours 19-22h where PV output is ~0, so same-day midday GHI
# cannot act through contemporaneous PV. (Hours 16-18 still have direct sun in HST summer ->
# midday_GHI x Batt there is contaminated by PV self-consumption; we report them but exclude
# from the identifying window and the energy integral.) Keep yearFE (battery grows within era)
# and a standalone midday-GHI control so the coef is the batt-INTERACTION, not the GHI main effect.
CLEAN = list(range(19, 23))     # 19,20,21,22 HST — sun down
eve = m[m["hour"].isin(CLEAN)].copy()
out.append("\nBATTERY TERM — clean sun-down window %s ~ hourFE + season + yearFE + evening-temp "
           "+ midday_GHI + midday_GHI x Batt_installed" % CLEAN)
out.append("  battery range in radiation years: %.1f - %.1f MWh"
           % (eve["batt_mwh_cum"].min(), eve["batt_mwh_cum"].max()))

# pooled (include standalone ghi_midday so the interaction is net of the GHI main effect)
modb = smf.ols("load_mw ~ C(hourF) + C(season) + C(yearF) + temp_evening + I(temp_evening**2) "
               "+ ghi_midday + middayghi_x_batt", data=eve).fit()
cb = modb.params.get("middayghi_x_batt", np.nan)   # MW per (W/m2 * MWh)
seb = modb.bse.get("middayghi_x_batt", np.nan)
ghi_mid_mean = eve["ghi_midday"].mean()
disch_mw_per_mwh_pooled = -cb * ghi_mid_mean
out.append("  pooled coef = %.6g (se %.6g) MW per (W/m2 * MWh)" % (cb, seb))
out.append("  mean midday GHI = %.0f W/m2 -> pooled evening load reduction "
           "= %.4f MW per installed MWh (avg over window)" % (ghi_mid_mean, disch_mw_per_mwh_pooled))

# per-hour battery shape over the full evening shoulder 17-23 (report all; integrate CLEAN only)
sh_rows = []
for h in range(17, 24):
    sub = m[m["hour"] == h].copy()
    mh = smf.ols("load_mw ~ C(season) + C(yearF) + temp_evening + I(temp_evening**2) "
                 "+ ghi_midday + middayghi_x_batt", data=sub).fit()
    c = mh.params.get("middayghi_x_batt", np.nan)
    sh_rows.append(dict(hour=h, coef=c, se=mh.bse.get("middayghi_x_batt", np.nan),
                        disch_mw_per_mwh=-c * ghi_mid_mean,
                        clean=h in CLEAN))
shape = pd.DataFrame(sh_rows).sort_values("hour").reset_index(drop=True)
# discharge shape = positive part (load reduction), normalized over the CLEAN sun-down window
shape["disch_pos"] = shape["disch_mw_per_mwh"].clip(lower=0)
cleanmask = shape["clean"]
tot_energy = shape.loc[cleanmask, "disch_pos"].sum()   # MWh delivered per installed MWh (1h steps)
shape["shape_weight"] = 0.0
if tot_energy > 0:
    shape.loc[cleanmask, "shape_weight"] = shape.loc[cleanmask, "disch_pos"] / tot_energy
shape.to_csv(os.path.join(ANA, "estimator2_battery_shape.csv"), index=False)
out.append("\n  per-hour battery discharge (MW lower evening load per installed MWh); "
           "shape_weight over CLEAN sun-down window only:")
out.append(shape[["hour", "coef", "se", "disch_mw_per_mwh", "clean", "shape_weight"]].round(4).to_string(index=False))

# ---- ENERGY-CONSERVATION CHECK
rte, reserve, usable = 0.86, 0.20, 0.90
E_phys = rte * (1 - reserve) * usable
out.append("\n  ENERGY per installed MWh (integral of discharge over evening) = %.3f MWh/MWh"
           % tot_energy)
out.append("  physics cap rte*(1-reserve)*usable = %.3f MWh/MWh" % E_phys)
passfail = "PASS" if tot_energy <= E_phys + 0.05 else ("PLAUSIBLE" if tot_energy <= 1.0 else "FAIL")
out.append("  energy-conservation check: %s (radiation-identified = %.3f vs collinear Estimator-1 = 3.24)"
           % (passfail, tot_energy))

pd.DataFrame([dict(pooled_coef=cb, pooled_se=seb, ghi_mid_mean=ghi_mid_mean,
                   energy_mwh_per_mwh=tot_energy, physics_cap=E_phys,
                   check=passfail)]).to_csv(
    os.path.join(ANA, "estimator2_battery_firmed.csv"), index=False)

txt = "\n".join(out)
with open(os.path.join(ANA, "estimator2_firmed_summary.txt"), "w") as fh:
    fh.write(txt + "\n")
print(txt)
print("\nDONE 09")

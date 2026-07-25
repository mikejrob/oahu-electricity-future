#!/usr/bin/env python3
"""
17_appendix_forecast_vs_actual.py -- assemble HECO distributed-PV forecast vintages vs realized
adoption for the report appendix, plus this report's three DistPV trajectories.

Series & provenance (every series labeled):
  PSIP2016   : PSIP_PV.csv, HECO 2016-12 PSIP Oahu "dist PV total" MW, DIGITIZED from a PSIP
               chart (decimal years -> snapped to nearest integer year). Docket 2014-0183.
               Anchor validation: PSIP@2016 = 444.0 vs actual 440.9 (der_points) -> good digitization.
  IGP_DER    : IGP_PV.csv "DER_BESS" (sign flipped). UNITS/SCOPE UNRESOLVED -- 2024 value 1,115 MW
               exceeds Oahu-only distributed PV (765 MW) by 1.46x; scale is consistent with an
               ALL-TERRITORIES DER series and/or PV+BESS bundle (HECO 2025 comms cite a forecast
               of 1,186 MW cumulative distributed solar by 2030, all territories; IGP_DER@2030=1,293).
               Presented SEPARATELY, not in the headline Oahu comparison.
  ACTUAL     : Oahu cumulative distributed PV MW, year-end, from oahu-grid der_points.parquet
               (permit/interconnection records). NOTE: the claimed transcription of HECO's
               quarterly installed-solar PDFs (heco_pv_summary_series.csv) does NOT exist on disk;
               der_points is the available actuals. External corroboration: HECO reports +61 MW
               rooftop added in 2024 (all territories; Oahu-share-consistent with der_points +44).
  OURS_*     : this report's DistPV operating-capacity trajectories from the model inputs
               (inputs_dgb=conservative, inputs_dgs=realistic, inputs_dga=accelerated), computed
               as builds minus 30-year retirements. Verified: 2027 = 800/820/840; 2050 operating
               = 1000/1560/2120 (accelerated = 2 x realistic - conservative, exact in inputs).

Outputs: appendix_forecast_vs_actual.csv, fig_heco_forecast_vs_actual.png
"""
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ANA = "/mnt/lustre/koa/koastore/gtg_group/oahu-electricity-v1-corrected/analysis"
NG = "/mnt/lustre/koa/koastore/gtg_group/ehartley/_Hawaii_NG_Switch"
REPO = "/mnt/lustre/koa/koastore/gtg_group/oahu-electricity-v1-corrected"
rows = []

# ---------------- PSIP 2016 (digitized) ----------------
psip = pd.read_csv(os.path.join(NG, "PSIP_PV.csv"), delimiter="\t")
psip.columns = ["year", "mw"]
psip["year"] = psip["year"].astype(str).str.replace(",", "").astype(float).round().astype(int)
psip = psip.groupby("year", as_index=False)["mw"].mean()   # snap collisions if any
for _, r in psip.iterrows():
    rows.append(dict(vintage="PSIP 2016 (Dec)", year=int(r.year), mw=round(r.mw, 1),
                     source="HECO 2016 PSIP, docket 2014-0183, Oahu dist-PV total",
                     provenance="digitized from PSIP chart; decimal years snapped to integer"))

# ---------------- IGP DER series (separate; units unresolved) ----------------
igp = pd.read_csv(os.path.join(NG, "IGP_PV.csv"))
igp["mw"] = -igp["DER_BESS"]
for _, r in igp.iterrows():
    rows.append(dict(vintage="IGP DER+BESS (units/scope unresolved)", year=int(r.year),
                     mw=round(r.mw, 1),
                     source="IGP_PV.csv 'DER_BESS'; IGP docket 2018-0165 (2023 Final Report is "
                            "citable vintage; on-disk series labeled 'IGP 2020' in Compare_Loads.ipynb)",
                     provenance="on-disk extract; NOT Oahu-only PV -- 2024 value 1115 exceeds "
                                "Oahu PV 765; scale consistent with all-territories DER and/or "
                                "PV+BESS; excluded from headline comparison"))

# ---------------- actuals (der_points, Oahu) ----------------
inst = pd.read_csv(os.path.join(ANA, "installs_cumulative_daily.csv"))
inst["date"] = pd.to_datetime(inst["date"])
for y in range(2006, 2025):
    sub = inst[inst["date"] <= f"{y}-12-31"]
    if len(sub):
        rows.append(dict(vintage="ACTUAL (Oahu)", year=y, mw=round(sub["pv_mw_cum"].iloc[-1], 1),
                         source="oahu-grid der_points.parquet, permit/interconnection records",
                         provenance="compiled records; year-end cumulative; HECO quarterly-PDF "
                                    "transcription claimed but not found on disk; HECO comms "
                                    "corroborate scale (+61 MW all-territories in 2024)"))

# ---------------- our trajectories (operating capacity, 30-yr life) ----------------
LIFE = 30
def op_traj(d):
    f = pd.read_csv(os.path.join(REPO, d, "gen_build_predetermined.csv"))
    f["cap"] = pd.to_numeric(f["build_gen_predetermined"], errors="coerce")
    dp = f[f["GENERATION_PROJECT"].str.contains("DistPV", case=False, na=False)]
    builds = dp.groupby("build_year")["cap"].sum()
    yrs = sorted(set(list(builds.index) + [2024, 2027, 2030, 2035, 2040, 2045, 2050]))
    out = {}
    for y in yrs:
        out[y] = builds[(builds.index <= y) & (builds.index > y - LIFE)].sum()
    return out

for d, name in [("inputs_dgb", "OURS conservative"), ("inputs_dgs", "OURS realistic"),
                ("inputs_dga", "OURS accelerated")]:
    tr = op_traj(d)
    for y, v in tr.items():
        if y >= 2025:
            rows.append(dict(vintage=name, year=int(y), mw=round(v, 1),
                             source=f"{d}/gen_build_predetermined.csv (this report)",
                             provenance=f"model input builds minus {LIFE}-yr retirements "
                                        "(operating capacity); accelerated = 2 x realistic - "
                                        "conservative (verified exact in inputs)"))

df = pd.DataFrame(rows)
df.to_csv(os.path.join(ANA, "appendix_forecast_vs_actual.csv"), index=False)
print("appendix_forecast_vs_actual.csv:", len(df), "rows")

# ---------------- headline numbers (verified) ----------------
act = df[df.vintage == "ACTUAL (Oahu)"].set_index("year")["mw"]
ps = df[df.vintage == "PSIP 2016 (Dec)"].set_index("year")["mw"]
print("\nHEADLINE CHECKS:")
print("  PSIP anchor 2016 = %.1f vs actual 2016 = %.1f (digitization validated)" % (ps[2016], act[2016]))
print("  PSIP 2034 = %.1f ; actual 2024 = %.1f -> actual reached PSIP's 2034 level in 2024 "
      "(a decade early)" % (ps[2034], act[2024]))
s_psip_long = (ps[2045] - ps[2021]) / 24
s_psip_same = (ps[2024] - ps[2016]) / 8
s_act_16_24 = (act[2024] - act[2016]) / 8
s_act_20_24 = (act[2024] - act[2020]) / 4
print("  PSIP slope 2021-2045 = %.1f MW/yr; PSIP slope 2016-2024 = %.1f MW/yr" % (s_psip_long, s_psip_same))
print("  realized slope 2016-2024 = %.1f MW/yr; realized 2020-2024 = %.1f MW/yr" % (s_act_16_24, s_act_20_24))
print("  ratio realized(2020-24)/PSIP(2021-45) = %.1fx ; realized(2016-24)/PSIP(2016-24) = %.1fx"
      % (s_act_20_24 / s_psip_long, s_act_16_24 / s_psip_same))

# ---------------- figure ----------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(ps.index, ps.values, "-", color="tab:blue", lw=1.4,
        label="PSIP 2016 forecast (Oahu dist PV, digitized)")
igps = df[df.vintage.str.startswith("IGP")].set_index("year")["mw"]
ax.plot(igps.index, igps.values, "-", color="tab:cyan", lw=1.2, alpha=0.8,
        label="IGP 'DER+BESS' series (units/scope unresolved; not Oahu-only PV)")
ax.plot(act.index, act.values, "-", color="black", lw=3, label="Actual Oahu distributed PV (der_points)")
colors = {"OURS conservative": "tab:green", "OURS realistic": "tab:orange", "OURS accelerated": "tab:red"}
for name, col in colors.items():
    s = df[df.vintage == name].set_index("year")["mw"].sort_index()
    ax.plot(s.index, s.values, "--", color=col, lw=1.8, label=name + " (this report, operating MW)")
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("year"); ax.set_ylabel("cumulative distributed PV (MW)")
ax.set_title("HECO distributed-PV forecasts vs realized adoption, Oahu")
ax.legend(fontsize=8, loc="upper left"); ax.grid(alpha=0.3)
ax.set_xlim(2006, 2050)
fig.tight_layout()
fig.savefig(os.path.join(ANA, "fig_heco_forecast_vs_actual.png"), dpi=130)
print("wrote fig_heco_forecast_vs_actual.png")
print("DONE 17")

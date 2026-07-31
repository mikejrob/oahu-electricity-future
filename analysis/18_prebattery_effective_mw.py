#!/usr/bin/env python3
"""Pre-battery calibration: effective usable AC MW per reported installed MW.

Purpose (see Appendix A.11): the installed-capacity series (pv_mw_cum,
compiled from permit/interconnection records) does not document its rating
basis (DC nameplate vs AC). All of the report's distributed-solar
coefficients are estimated per *reported* MW on this same series, so the
net-load projections are internally consistent whatever the basis. This
script pins the physical interpretation: in the pre-battery, NEM era
(2013-2019), when essentially all rooftop generation appeared on the meter,
the grid-load reduction per reported MW at reference irradiance (1 kW/m2)
measures usable AC output per reported MW, bundling tilt, aspect, soiling,
and inverter conversion.

Design: 4-hour blocks (averaging reduces measurement noise and attenuation
bias); day-to-day island-mean GHI variation within block x season x year
identifies the response; temperature controls; errors clustered by month.
Zone-weighting of radiation by installed MW is immaterial for this fleet
(weighted/uniform ratio 0.9907; analysis/TASK_B_NOTES.md).

Result (written to prebattery_effective_mw.txt): ~0.79 usable AC MW per
reported MW (se ~0.03), consistent with a DC-nameplate reported series and
standard derates. Not directly comparable to the battery-era 0.61 MW/MW
grid-load coefficient, which additionally nets the behind-the-meter wedge
and post-NEM tariff structures.
"""
import pandas as pd
import statsmodels.formula.api as smf

ANA = "/mnt/lustre/koa/koastore/gtg_group/oahu-electricity-v1-corrected/analysis"

p = pd.read_parquet(f"{ANA}/panel_hourly_with_installs.parquet")
r = pd.read_parquet(f"{ANA}/nsrdb_oahu_island_hourly_2013_2019.parquet")
r = r[["year", "month", "day", "hour", "ghi", "temp"]].drop_duplicates(
    ["year", "month", "day", "hour"])

p["dt"] = pd.to_datetime(p.dt_hst).dt.tz_localize(None)
p["y"], p["m"], p["d"], p["h"] = p.dt.dt.year, p.dt.dt.month, p.dt.dt.day, p.dt.dt.hour
d = p.merge(r, left_on=["y", "m", "d", "h"],
            right_on=["year", "month", "day", "hour"], how="inner")
d = d[(d.y >= 2013) & (d.y <= 2019)]           # pre-battery, NEM era; also the
                                               # FERC-714 reference clock era
d["blk"] = (d.h // 4) * 4
d["ghi_kw"] = d.ghi / 1000.0

g = (d.groupby(["y", "m", "d", "blk"])
       .agg(load=("load_mw", "mean"), ghi=("ghi_kw", "mean"),
            temp=("temp", "mean"), pv=("pv_mw_cum", "mean"),
            batt=("batt_mwh_cum", "mean")).reset_index())
g["ghi_pv"] = g.ghi * g.pv
g["season"] = (g.m % 12) // 3

day = g[g.blk.isin([8, 12, 16])].copy()        # daylight blocks
day["blk_s"] = day.blk.astype(str) + "_" + day.season.astype(str)

mod = smf.ols("load ~ ghi_pv + ghi + temp + C(blk_s) + C(y)", data=day).fit(
    cov_type="cluster",
    cov_kwds={"groups": day.y.astype(str) + "-" + day.m.astype(str)})

b, se = mod.params["ghi_pv"], mod.bse["ghi_pv"]
out = (
    f"Pre-battery effective usable AC MW per reported installed MW\n"
    f"window 2013-2019 (NEM era; max batt/PV ratio "
    f"{g.batt.max()/g.pv.max():.3f} MWh/MW)\n"
    f"4-hour daylight blocks, N={len(day)}\n"
    f"GHI x PV coefficient: {b:.4f} (se {se:.4f}), month-clustered\n"
    f"-> {-b:.3f} MW grid-load reduction per reported MW at 1 kW/m2\n"
    f"Interpretation: usable AC output per reported MW incl. tilt/aspect/\n"
    f"soiling/inverter; consistent with a DC-nameplate reported series.\n"
)
open(f"{ANA}/prebattery_effective_mw.txt", "w").write(out)
print(out)

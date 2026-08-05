#!/usr/bin/env python3
"""Derive a part-load fuel curve for the JERA plant from EPA CEMS records.

Usage: python3 build/derive_jera_partload_from_cems.py <path-to-epacems-parquet>
See sources/epa_cems/README.md for sources, criteria, and the applied curve.

Fleet: mainland natural-gas combined-cycle combustion turbines in the
F-class capacity range (140-260 MW nameplate, vintage 2002+), selected from
EIA-860 via PUDL and matched to CAMD units through the EPA-EIA crosswalk
(candidates.csv). For each unit, hourly gross load and heat input
(2022-2024) give an input-output line fit on steady full-hour operation;
the fleet-median normalized shape (no-load fuel share, incremental slope
profile, realized minimum stable load) is then rescaled onto the model's
125 MW JERA blocks anchored at the sourced 6.92 MMBtu/MWh full-load rate.

Outputs: unit_fits.csv (per-unit parameters), fleet summary to stdout,
and proposed gen_inc_heat_rates.csv rows for the four JERA blocks.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.dataset as ds

REPO = Path(__file__).resolve().parent.parent

YEARS = [2022, 2023, 2024]
SEG_EDGES = np.array([0.40, 0.55, 0.70, 0.85, 1.00])  # segment bounds, share of Lmax
MIN_HOURS = 2000       # minimum steady operating hours to fit a unit
RAMP_TOL = 0.15        # steady = neighbors within 15% of Lmax
FULL_LOAD_HR = 6.92    # MMBtu/MWh, sourced anchor for the JERA plant
BLOCK_MW = 125.0

cand = pd.read_csv(REPO / "sources/epa_cems/candidates.csv")
plants = sorted(cand.plant_id_eia.unique())

print(f"extracting {len(plants)} plants, years {YEARS} ...")
dataset = ds.dataset(sys.argv[1] if len(sys.argv) > 1 else "core_epacems__hourly_emissions.parquet", format="parquet")
tab = dataset.to_table(
    columns=["plant_id_eia", "emissions_unit_id_epa", "operating_datetime_utc",
             "operating_time_hours", "gross_load_mw", "heat_content_mmbtu", "year"],
    filter=(ds.field("year").isin(YEARS)) & (ds.field("plant_id_eia").isin(plants)))
df = tab.to_pandas()
print(f"  {len(df):,} unit-hours")

# keep only the matched CT units (a plant may have other CEMS units)
key = set(zip(cand.plant_id_eia, cand.emissions_unit_id_epa.astype(str)))
df = df[[(p, u) in key for p, u in
         zip(df.plant_id_eia, df.emissions_unit_id_epa.astype(str))]]
print(f"  {len(df):,} after matching CT units ({df.emissions_unit_id_epa.nunique()} unit ids)")

fits = []
for (pid, uid), g in df.groupby(["plant_id_eia", "emissions_unit_id_epa"]):
    g = g.sort_values("operating_datetime_utc")
    op = g[(g.operating_time_hours >= 0.99) & (g.gross_load_mw > 0)
           & (g.heat_content_mmbtu > 0)].copy()
    if len(op) < MIN_HOURS:
        continue
    lmax = op.gross_load_mw.quantile(0.99)
    # steady hours: both neighbors present and within RAMP_TOL of Lmax
    d_prev = (op.gross_load_mw - op.gross_load_mw.shift(1)).abs()
    d_next = (op.gross_load_mw - op.gross_load_mw.shift(-1)).abs()
    steady = op[(d_prev <= RAMP_TOL * lmax) & (d_next <= RAMP_TOL * lmax)
                & (op.gross_load_mw >= 0.25 * lmax)
                & (op.gross_load_mw <= 1.02 * lmax)]
    if len(steady) < MIN_HOURS:
        continue
    share = steady.gross_load_mw / lmax
    min_share = share.quantile(0.02)
    # binned medians across the observed load range, then a line through them
    bins = np.linspace(max(0.30, min_share), 1.0, 15)
    idx = np.digitize(share, bins)
    pts = []
    for b in range(1, len(bins)):
        sel = steady[idx == b]
        if len(sel) >= 50:
            pts.append((sel.gross_load_mw.median(), sel.heat_content_mmbtu.median(),
                        len(sel)))
    if len(pts) < 6:
        continue
    P = np.array(pts)
    w = np.sqrt(P[:, 2])
    A = np.vstack([np.ones(len(P)), P[:, 0]]).T
    coef, *_ = np.linalg.lstsq(A * w[:, None], P[:, 1] * w, rcond=None)
    a, b = coef                      # heat = a + b * load
    if a <= 0 or b <= 0:
        continue                     # non-physical fit (apportionment artifacts)
    fuel_full = a + b * lmax
    seg_hr = {}
    for lo, hi in zip(SEG_EDGES[:-1], SEG_EDGES[1:]):
        sel = steady[(share >= lo) & (share < hi)]
        seg_hr[f"hr_{int(lo*100)}_{int(hi*100)}"] = (
            (sel.heat_content_mmbtu.sum() / sel.gross_load_mw.sum())
            if len(sel) >= 100 else np.nan)
    fits.append({
        "plant_id_eia": pid, "unit": uid, "hours": len(steady), "lmax_mw": lmax,
        "min_share": min_share, "alpha": a / fuel_full,
        "hr_full": fuel_full / lmax,
        "hr_50": (a + b * 0.5 * lmax) / (0.5 * lmax),
        "hr_75": (a + b * 0.75 * lmax) / (0.75 * lmax),
        **seg_hr})

f = pd.DataFrame(fits)
f.to_csv(REPO / "sources/epa_cems/unit_fits.csv", index=False)
print(f"\nfitted {len(f)} units at {f.plant_id_eia.nunique()} plants")
med = f.median(numeric_only=True)
q1, q3 = f.quantile(0.25, numeric_only=True), f.quantile(0.75, numeric_only=True)
for k in ("alpha", "min_share", "hr_full", "hr_50", "hr_75"):
    print(f"  {k:10s} median {med[k]:.3f}   IQR [{q1[k]:.3f}, {q3[k]:.3f}]")
print(f"  part-load penalty at 50%: {med['hr_50']/med['hr_full']-1:+.1%}, "
      f"at 75%: {med['hr_75']/med['hr_full']-1:+.1%}")

# ---- map onto the JERA 125 MW blocks, anchored at FULL_LOAD_HR ----
alpha = med["alpha"]
# applied minimum load: 50% policy choice (author, 2026-08-02) — just below
# the fleet median 52%, inside the 45-58% IQR; no block turndown figure in
# the JERA proposal contradicts it (sources/epa_cems/README.md)
min_share = 0.50
fuel_full = FULL_LOAD_HR * BLOCK_MW
a_j = alpha * fuel_full
b_j = (1 - alpha) * fuel_full / BLOCK_MW
lmin = min_share * BLOCK_MW
print(f"\nproposed JERA block curve (anchor {FULL_LOAD_HR} MMBtu/MWh at {BLOCK_MW:.0f} MW):")
print(f"  min load {lmin} MW (fleet-median realized min share {min_share:.2f})")
print(f"  no-load fuel {a_j:.1f} MMBtu/h (alpha {alpha:.3f}); incremental {b_j:.3f} MMBtu/MWh")
print(f"  avg HR: at min {(a_j + b_j*lmin)/lmin:.2f}, at 50% {(a_j+b_j*62.5)/62.5:.2f}, "
      f"at 75% {(a_j+b_j*93.75)/93.75:.2f}, at full {FULL_LOAD_HR:.2f}")
print("\nproposed gen_inc_heat_rates.csv rows (per block):")
print(f"Oahu_JERA,{lmin:g},.,.,{a_j + b_j*lmin:.1f}")
edges = [lmin, 75, 100, 125]
edges = sorted(set(e for e in edges if e >= lmin))
for lo, hi in zip(edges[:-1], edges[1:]):
    print(f"Oahu_JERA,{lo}.0,{hi}.0,{b_j:.3f},.")

#!/usr/bin/env python3
"""
Market-based Brent oil-price band (5th/95th percentiles) for the Oahu electricity report.

Construction (author's spec):
  1. Take the ICE Brent futures strip (nominal USD/bbl) by contract month.
  2. For each contract i with futures price F_i and ATM implied vol sigma(tau_i)
     (tau_i = years from quote date t0 to option/futures expiry), the lognormal
     ATM 5th/95th percentiles of the terminal futures price are
        P5_i  = F_i * exp(-1.645 * sigma_i * sqrt(tau_i))
        P95_i = F_i * exp(+1.645 * sigma_i * sqrt(tau_i))
  3. Deflate each percentile to real 2024$ with a deflator built from realized
     CPI-U (2024 avg -> latest print) chained to TIPS breakeven expected
     inflation (5y breakeven for the first 5 years from t0, 5y5y forward after).
  4. Fit smooth lines through the real 5th and 95th series across contract
     delivery dates (PCHIP through the monthly strip = primary; cubic
     least-squares polynomial reported as sensitivity).
  5. Extend beyond the last listed contract FLAT IN REAL TERMS (near-unit-root,
     zero real drift).
  6. Average the smoothed lines over each Switch model period's calendar years:
     2027-29, 2030-34, 2035-39, 2040-44, 2045-49, 2050-54.

All market inputs are saved raw under sources/market/raw/ with quote dates.
See sources/market/METHOD.md for sources, equations, and assumptions.

Run:  python3 build/market_band/build_market_percentiles.py
Outputs (sources/market/):
  brent_market_percentiles.csv            per-period low/high real-2024$ Brent
  brent_market_percentiles_contracts.csv  per-contract underlying table
  brent_market_band.png                   figure
"""
import csv
import datetime as dt
import os

import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

REPO = "/mnt/lustre/koa/koastore/gtg_group/oahu-electricity-v1-corrected"
RAW = os.path.join(REPO, "sources", "market", "raw")
OUT = os.path.join(REPO, "sources", "market")

# ----------------------------------------------------------------------------
# Dated market parameters (every number traceable to a file in sources/market/raw/
# or to a cited press/EIA source; see METHOD.md)
# ----------------------------------------------------------------------------
T0 = dt.date(2026, 7, 27)          # quote date of the futures strip (oilprice.com pull)

# Implied volatility term structure (annualized, ATM lognormal):
# sigma(tau) = SIGMA_LONG + (OVX - SIGMA_CALM_1M) * exp(-K_DECAY * (tau_days - 30))
# - OVX = 0.680 : Cboe Crude Oil ETF (USO/WTI) 30-day IV, 2026-07-24 close
#   (raw/fred_OVXCLS_pulled_20260727.csv). War-elevated front tenor.
# - SIGMA_CALM_1M = 0.312 : calm-regime 1-month WTI ATM IV, NYMEX options,
#   five trading days ending 2025-09-04 (EIA STEO probability workbook,
#   raw/eia_steo_probability_WTI_july2026_pulled_2026-07-27.xlsx). The same
#   workbook shows 0.268 at the ~10-month tenor.
# - K_DECAY = 0.033/day : exponential decay of the war/event premium with
#   tenor, calibrated to the March 2026 escalation episode reported by
#   Reuters (30-day ATM Brent IV +17.5 pts while 60-day +5.9 and 90-day
#   +2.8 pts => premium ratios 0.34 @60d, 0.16 @90d => k ~ 0.031-0.036/day).
# - SIGMA_LONG = 0.30 : documented ASSUMPTION for tenors >= ~12 months, held
#   FLAT to the last contract (no liquid quotes observable; see METHOD.md).
#   Sensitivity run at 0.25 / 0.35.
OVX = 0.680
SIGMA_CALM_1M = 0.312
K_DECAY = 0.033
SIGMA_LONG = 0.30
SIGMA_SENS = (0.25, 0.35)
Z90 = 1.645                        # two-sided 90% band => 5th/95th percentiles

# Inflation (deflate nominal USD at date T to real 2024$):
# realized CPI-U: 2024 annual avg 313.698, latest print 332.568 (2026-06-01),
# raw/fred_CPIAUCSL_pulled_20260727.csv
CPI_2024_AVG = 313.698
CPI_LATEST = 332.568
# TIPS breakevens, 2026-07-27 (raw/fred_T5YIE|T5YIFR|T10YIE_pulled_20260727.csv)
BE_5Y = 0.0218                     # T5YIE
BE_5Y5Y = 0.0224                   # T5YIFR (5y5y forward)

# Switch model periods (calendar years covered by each investment period)
PERIODS = {
    "2027-29": (2027, 2029), "2030-34": (2030, 2034), "2035-39": (2035, 2039),
    "2040-44": (2040, 2044), "2045-49": (2045, 2049), "2050-54": (2050, 2054),
}
# Model period label -> representative period start year used in fuel_supply_curves
PERIOD_KEY_YEAR = {"2027-29": 2027, "2030-34": 2030, "2035-39": 2035,
                   "2040-44": 2040, "2045-49": 2045, "2050-54": 2050}

# EIA AEO-derived reference/low/high LSFO base-tier prices (real 2024$/MMBtu)
# from inputs/fuel_supply_curves*.csv; implied Brent via inverse of the
# LSFO regression: LSFO $/bbl = 37.30 + 0.7388 * Brent, 6.22 MMBtu/bbl.
LSFO_BASE = {  # period-start-year: (ref, low, high)
    2027: (16.622193, 16.622193, 16.622193),
    2030: (16.721495, 16.060488, 17.736064),
    2035: (17.041535, 15.226249, 19.827788),
    2040: (17.323071, 14.298038, 21.966145),
    2045: (17.777086, 13.420682, 24.463659),
    2050: (18.730092, 12.713254, 27.965238),
}
def lsfo_to_brent(p_mmbtu):
    return (p_mmbtu * 6.22 - 37.30) / 0.7388

# ----------------------------------------------------------------------------
# Load the futures strip
# ----------------------------------------------------------------------------
def load_strip():
    path = os.path.join(RAW, "oilprice_brent_futures_strip_pulled_2026-07-27.csv")
    rows = []
    with open(path) as f:
        for r in csv.DictReader(l for l in f if not l.startswith("#")):
            mon, yr = r["expiry_month_year"].split()
            m = dt.datetime.strptime(mon, "%b").month
            rows.append((r["contract_code"], int(yr), m, float(r["last_price"])))
    return pd.DataFrame(rows, columns=["code", "dyear", "dmonth", "F"])

def month_end(y, m):
    nxt = dt.date(y + m // 12, m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)

def sigma_of(tau_days):
    prem = (OVX - SIGMA_CALM_1M) * np.exp(-K_DECAY * np.maximum(tau_days - 30.0, 0.0))
    return SIGMA_LONG + prem

def cum_infl_factor(years_ahead):
    """Expected cumulative inflation factor from t0 to t0+years_ahead (breakevens)."""
    y1 = np.minimum(years_ahead, 5.0)
    y2 = np.maximum(years_ahead - 5.0, 0.0)
    return (1 + BE_5Y) ** y1 * (1 + BE_5Y5Y) ** y2

def deflator_to_2024(delivery_date):
    """Divide nominal $ at delivery_date by this to get real 2024$."""
    yrs = (delivery_date - T0).days / 365.25
    return (CPI_LATEST / CPI_2024_AVG) * cum_infl_factor(max(yrs, 0.0))

# ----------------------------------------------------------------------------
def build(sigma_long_override=None):
    global SIGMA_LONG
    saved = SIGMA_LONG
    if sigma_long_override is not None:
        SIGMA_LONG = sigma_long_override
    df = load_strip()
    # ICE Brent: trading in delivery month M ceases at the end of month M-2
    df["expiry"] = [month_end(y if m > 2 else y - 1, (m - 2 - 1) % 12 + 1)
                    for y, m in zip(df.dyear, df.dmonth)]
    df["delivery"] = [dt.date(y, m, 15) for y, m in zip(df.dyear, df.dmonth)]
    df["tau_yr"] = [(e - T0).days / 365.25 for e in df.expiry]
    df = df[df.tau_yr > 0].reset_index(drop=True)
    df["sigma"] = sigma_of(df.tau_yr.values * 365.25)
    w = Z90 * df.sigma * np.sqrt(df.tau_yr)
    df["p5_nom"] = df.F * np.exp(-w)
    df["p95_nom"] = df.F * np.exp(w)
    df["deflator"] = [deflator_to_2024(d) for d in df.delivery]
    for c in ("F", "p5", "p95"):
        src = "F" if c == "F" else c + "_nom"
        df[c + "_real24"] = df[src] / df.deflator
    SIGMA_LONG = saved
    return df

def period_averages(df):
    """Smooth lines through real percentiles vs delivery date; average by period."""
    x = np.array([(d - T0).days / 365.25 for d in df.delivery])
    fits = {c: PchipInterpolator(x, df[c + "_real24"].values) for c in ("F", "p5", "p95")}
    x_last = x[-1]
    # monthly grid 2027-01 .. 2054-12
    months = pd.date_range("2027-01-15", "2054-12-15", freq="MS") + pd.Timedelta(days=14)
    xg = np.array([(m.date() - T0).days / 365.25 for m in months])
    grid = {c: np.where(xg <= x_last, f(np.minimum(xg, x_last)), f(x_last))
            for c, f in fits.items()}
    out = []
    for label, (y0, y1) in PERIODS.items():
        sel = (months.year >= y0) & (months.year <= y1)
        out.append({"period": label,
                    "brent_low_5th": grid["p5"][sel].mean(),
                    "brent_central_futures": grid["F"][sel].mean(),
                    "brent_high_95th": grid["p95"][sel].mean()})
    return pd.DataFrame(out), months, grid

def poly_period_averages(df, deg=3):
    """Sensitivity: cubic least-squares fit instead of PCHIP."""
    x = np.array([(d - T0).days / 365.25 for d in df.delivery])
    months = pd.date_range("2027-01-15", "2054-12-15", freq="MS") + pd.Timedelta(days=14)
    xg = np.array([(m.date() - T0).days / 365.25 for m in months])
    res = {}
    for c in ("p5", "p95"):
        cf = np.polyfit(x, df[c + "_real24"].values, deg)
        yv = np.polyval(cf, np.minimum(xg, x[-1]))
        res[c] = yv
    out = []
    for label, (y0, y1) in PERIODS.items():
        sel = (months.year >= y0) & (months.year <= y1)
        out.append({"period": label, "p5_poly3": res["p5"][sel].mean(),
                    "p95_poly3": res["p95"][sel].mean()})
    return pd.DataFrame(out)

def main():
    df = build()
    per, months, grid = period_averages(df)
    per_poly = poly_period_averages(df)
    sens = {}
    for s in SIGMA_SENS:
        d2 = build(sigma_long_override=s)
        p2, _, _ = period_averages(d2)
        sens[s] = p2

    # EIA AEO-implied Brent by period (real 2024$)
    eia = pd.DataFrame(
        [{"period": lbl,
          "eia_ref_brent": lsfo_to_brent(LSFO_BASE[yr][0]),
          "eia_low_brent": lsfo_to_brent(LSFO_BASE[yr][1]),
          "eia_high_brent": lsfo_to_brent(LSFO_BASE[yr][2])}
         for lbl, yr in PERIOD_KEY_YEAR.items()])
    per = per.merge(eia, on="period")
    for s in SIGMA_SENS:
        per[f"low_sigma{s:.2f}"] = sens[s]["brent_low_5th"].values
        per[f"high_sigma{s:.2f}"] = sens[s]["brent_high_95th"].values
    per = per.merge(per_poly, on="period")

    hdr = (f"# Market-based Brent 5th/95th percentile band, real 2024$/bbl.\n"
           f"# Built {dt.date.today()} from futures strip quoted {T0} "
           f"(see sources/market/METHOD.md and raw/ for provenance).\n"
           f"# sigma_long={SIGMA_LONG}, OVX(2026-07-24)={OVX}, calm 1m IV={SIGMA_CALM_1M}"
           f" (EIA, 2025-09-04), war-premium decay k={K_DECAY}/day.\n"
           f"# Breakevens 2026-07-27: 5y={BE_5Y:.4f}, 5y5y fwd={BE_5Y5Y:.4f}; "
           f"CPI-U 2024avg={CPI_2024_AVG}, latest(2026-06)={CPI_LATEST}.\n"
           f"# Periods 2035+ = flat-in-real extension of the fitted lines "
           f"beyond the last listed contract (Jan 2035).\n")
    p_out = os.path.join(OUT, "brent_market_percentiles.csv")
    with open(p_out, "w") as f:
        f.write(hdr)
        per.round(2).to_csv(f, index=False)

    c_out = os.path.join(OUT, "brent_market_percentiles_contracts.csv")
    with open(c_out, "w") as f:
        f.write("# Per-contract table underlying brent_market_percentiles.csv. "
                "Futures strip: oilprice.com pull 2026-07-27 (ICE Brent).\n")
        df.round(4).to_csv(f, index=False)

    # ---- figure ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 6))
    xd = [pd.Timestamp(d) for d in df.delivery]
    ax.plot(xd, df.F_real24, "k.-", lw=1, ms=3, label="Brent futures strip (real 2024$)")
    ax.plot(xd, df.p5_real24, "v", color="tab:blue", ms=4, label="5th pct (per contract)")
    ax.plot(xd, df.p95_real24, "^", color="tab:red", ms=4, label="95th pct (per contract)")
    ax.plot(months, grid["p5"], "-", color="tab:blue", lw=1.5, label="5th pct smoothed + flat ext.")
    ax.plot(months, grid["p95"], "-", color="tab:red", lw=1.5, label="95th pct smoothed + flat ext.")
    ax.plot(months, grid["F"], "--", color="gray", lw=1, label="futures smoothed + flat ext.")
    for lbl, (y0, y1) in PERIODS.items():
        yr = PERIOD_KEY_YEAR[lbl]
        xs = [pd.Timestamp(f"{y0}-01-01"), pd.Timestamp(f"{y1}-12-31")]
        for col, colr, lab in (("eia_ref_brent", "green", "EIA AEO ref (implied)"),
                               ("eia_low_brent", "olive", "EIA AEO low (implied)"),
                               ("eia_high_brent", "darkorange", "EIA AEO high (implied)")):
            v = per.loc[per.period == lbl, col].iloc[0]
            ax.plot(xs, [v, v], color=colr, lw=2,
                    label=lab if lbl == "2027-29" else None)
    ax.set_ylabel("Brent, real 2024 $/bbl")
    ax.set_title(f"Market-implied Brent 5th-95th band (futures {T0}, ATM lognormal, "
                 f"sigma_long={SIGMA_LONG})")
    ax.legend(fontsize=8, ncol=2)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "brent_market_band.png"), dpi=150)

    print(per.round(1).to_string(index=False))
    print("\nWrote:", p_out, c_out, os.path.join(OUT, "brent_market_band.png"))

if __name__ == "__main__":
    main()

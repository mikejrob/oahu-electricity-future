# Market-based Brent oil-price band: method and provenance

Built 2026-07-27. Reconstruction script: `build/market_band/build_market_percentiles.py`
(pure function of the raw files listed below plus the parameters documented here).
Outputs: `brent_market_percentiles.csv` (per-period band), `brent_market_percentiles_contracts.csv`
(per-contract detail), `brent_market_band.png` (figure).

## Purpose

Use futures and options markets to pin down the market-implied 5th and 95th
percentiles of the Brent price for every listed contract date, deflate to real
2024$, fit smooth lines, and average over the Switch model periods
(2027–29, 2030–34, 2035–39, 2040–44, 2045–49, 2050–54) to produce one low and
one high real-2024$ Brent number per period.

## Data sources (all raw pulls saved in `sources/market/raw/`)

| Input | Source, quote date | File |
|---|---|---|
| Brent futures strip, Sep 2026–Jan 2035 (monthly) | oilprice.com Brent futures table (ICE Brent), quoted 16:07 2026-07-27 | `oilprice_brent_futures_strip_pulled_2026-07-27.csv` |
| Cross-check of far strip (Dec 2027–Dec 2034) | TradingView ICE Futures Europe contract pages, 2026-07-27 | `tradingview_brent_dec_contracts_crosscheck_pulled_2026-07-27.md` |
| Front-tenor implied vol: OVX (Cboe Crude Oil ETF 30-day IV) = 68.00, 2026-07-24 close | FRED `OVXCLS` | `fred_OVXCLS_pulled_20260727.csv` |
| Calm-regime WTI IV term structure: 31.2% (1m) → 26.8% (10m), NYMEX options, 5 days ending 2025-09-04 | EIA STEO "WTI crude oil probabilities" workbook (link current on EIA STEO global-oil page as of 2026-07-27; workbook vintage Sep 2025) | `eia_steo_probability_WTI_july2026_pulled_2026-07-27.xlsx` |
| War-premium tenor decay: front 30d IV +17.5 pts vs +5.9 (60d), +2.8 (90d) in March 2026 escalation | Reuters via Yahoo Finance, 2026-03-06; Saxo 2026-07-20; Sharpe Two 2026-07-26 | `press_iv_notes_pulled_2026-07-27.md` |
| Inflation breakevens: 5y = 2.18%, 5y5y fwd = 2.24% (10y = 2.21%), 2026-07-27 | FRED `T5YIE`, `T5YIFR`, `T10YIE` | `fred_T5YIE/T5YIFR/T10YIE_pulled_20260727.csv` |
| Realized CPI-U: 2024 avg 313.698; latest print 332.568 (June 2026) | FRED `CPIAUCSL` | `fred_CPIAUCSL_pulled_20260727.csv` |
| Context: EIA STEO July 2026 WTI spot forecast + NYMEX futures curve (5 days ending 2026-07-01) | EIA STEO July 2026, Fig. 1 | `eia_steo_july2026_Fig1_wti_price_futures_pulled_2026-07-27.xlsx` |

Strip quality. The oilprice.com and TradingView pulls agree to the cent for
Dec 2030–Dec 2034 (70.72, 70.13, 69.57, 68.73, 68.02) and within $0.31 for
Dec 2027–Dec 2029 (intraday timing), so the far strip is an exchange
settlement echo, not aggregator interpolation. Far contracts trade thinly;
their settlements are exchange-assessed. Attempts to pull the primary CME
settlement CSV (`cmegroup.com/ftp/pub/settle/nymex_future.csv`) timed out
repeatedly (from both fetch paths); ino.com was unreachable; ICE end-of-day
reports and Barchart/QuikStrike option pages are JS/login-gated. Documented gap:
no primary-exchange file; the two independent aggregator echoes above are used
instead. The strip fetch returned contracts through Jan 2035 (page lists to
Jan 2036); the band beyond the last contract is a flat extension anyway.

Market context on the quote date: prompt Brent ≈ $88–91 with an active
war/Strait-of-Hormuz risk premium; strip steeply backwardated to ≈ $68–70
(nominal) by 2033–35; OVX at 68 (vs ~30 in calm markets).

## Construction

Quote date t0 = 2026-07-27. For each listed contract i (delivery month M_i):

- Expiry: ICE Brent trading ceases at the end of the second month before
  delivery; expiry_i = last day of M_i − 2 (matches exchange last-trade dates
  2027-10-29 / 2034-10-31 in the TradingView pull). Tenor
  τ_i = (expiry_i − t0)/365.25.
- ATM lognormal percentiles (nominal):
  P5_i = F_i·exp(−1.645·σ(τ_i)·√τ_i),  P95_i = F_i·exp(+1.645·σ(τ_i)·√τ_i).
- Implied vol term structure:
  σ(τ) = σ_long + (OVX − σ_calm,1m)·exp(−k·(τ_days − 30)),
  with OVX = 0.680 (2026-07-24), σ_calm,1m = 0.312 (EIA, 2025-09-04),
  k = 0.033/day (fit to the March 2026 premium decay: ratios 0.34 at 60d,
  0.16 at 90d ⇒ k ≈ 0.031–0.036), σ_long = 0.30 (assumption, below).
  Effective values: σ(Dec-2026) = 0.342; σ ≈ 0.300 for Dec-2027 onward.
- Deflation to real 2024$ (per-contract, dated at the delivery month):
  deflator(T) = (CPI_Jun2026 / CPI_2024avg) · (1+0.0218)^min(Δ,5) · (1+0.0224)^max(Δ−5,0),
  Δ = years from t0 to delivery. Realized CPI covers 2024→June 2026 (factor
  1.0602); TIPS breakevens cover t0 forward (5y breakeven for the first five
  years, 5y5y forward beyond). The ~2-month seam between the June CPI print
  and t0 is left uncounted (≈0.3% understatement of the deflator; direction:
  raises all real values ~0.3%, negligible).
- Smoothing: monotone PCHIP through the full monthly strip of real 5th/95th
  values as a function of delivery date (the series is already smooth; a cubic
  least-squares fit is reported alongside as `p5_poly3`/`p95_poly3` and agrees
  within ~$2).
- Extension: beyond the last listed contract (Jan 2035 delivery), both lines
  are held FLAT IN REAL TERMS (near-unit-root price process, zero real drift;
  the band width is frozen at the ~8.4-year tenor rather than continuing to
  widen as √t — a narrowing choice relative to a pure random walk, and the
  author's specified treatment).
- Period averages: monthly grid Jan 2027–Dec 2054, averaged over each model
  period's calendar years.

## Assumptions and their direction of effect

1. **σ_long = 0.30 for tenors ≥ ~12 months (held flat to 8.4y) — the main
   assumption.** No current (July 2026) market quote for 12m+ ATM Brent/WTI IV
   was publicly obtainable (gap documented above). Anchors: (i) the only
   measured long-tenor point, 26.8% at the 10-month tenor in a calm regime
   (EIA workbook, Sep 2025); (ii) evidence that war premia decay fast with
   tenor (March 2026: +17.5 pts at 30d vs +2.8 at 90d), implying a small
   (≲3 pt) residual war increment at 12m. 0.30 ≈ calm 0.27 + ~3 pts.
   Holding σ flat beyond the last observable tenor ignores the usual
   Samuelson/mean-reversion decline of long-dated IV (historically toward
   ~20–25%), so it is conservative-WIDE at long horizons. Sensitivity columns
   in the output: σ_long = 0.25 and 0.35 (2035+ band: 16/175 and 10/281 vs
   central 13/222 real 2024$).
2. **ATM lognormal percentiles rather than the full smile.** Current
   front-tenor options carry extreme call skew (war pricing), so the ATM
   approximation understates today's upside tail at the front tenors
   (≲ Dec-2026, which barely enter the period averages); at long tenors skew
   is milder and the approximation is roughly neutral. No smile data are
   publicly fetchable; documented approximation.
3. **OVX (WTI-ETF vol) as the front-tenor proxy for Brent vol.** Brent and WTI
   30-day IV track within a few points (the March episode article reports
   Brent 30d IV 68 at the same time OVX printed similar levels in July).
   Front tenor has almost no effect on the period averages.
4. **Risk-neutral percentiles read as physical.** Options prices give the
   risk-neutral distribution; variance risk premia mean risk-neutral tails are
   somewhat wider than physical forecasts — direction: conservative-wide on
   both sides.
5. **Breakeven mapping.** TIPS breakevens embed an inflation risk premium and
   are CPI-U-based (matching the CPI deflator used); horizon-matching is
   5y breakeven then 5y5y forward (the 10y breakeven, 2.21%, is consistent).
6. **Stale-vintage EIA workbook.** The EIA "WTI probabilities" workbook linked
   from the current STEO page is the Sep-2025 vintage; it is used only as the
   calm-regime IV anchor, dated as such, not as a current quote.

## Result (real 2024$/bbl Brent)

| Period | Market 5th | Futures (central) | Market 95th | EIA-implied ref | EIA-implied low | EIA-implied high |
|---|---|---|---|---|---|---|
| 2027–29 | 35.5 | 66.7 | 128.4 | 89.5 | 89.5 | 89.5 |
| 2030–34 | 18.1 | 57.9 | 189.1 | 90.3 | 84.7 | 98.8 |
| 2035–39 | 12.8 | 53.3 | 221.7 | 93.0 | 77.7 | 116.4 |
| 2040–44 | 12.8 | 53.3 | 221.7 | 95.4 | 69.9 | 134.4 |
| 2045–49 | 12.8 | 53.3 | 221.7 | 99.2 | 62.5 | 155.5 |
| 2050–54 | 12.8 | 53.3 | 221.7 | 107.2 | 56.5 | 185.0 |

EIA-implied columns invert the model's base-tier LSFO price
(`inputs/fuel_supply_curves*.csv`): Brent = (LSFO$/MMBtu·6.22 − 37.30)/0.7388.

Comparison with the AEO-derived case spread used in the model:
- The market 95th is far above the EIA-implied reference in every period
  (128 vs 90 in 2027–29; 222 vs 93–107 from 2035 on) and above the EIA-implied
  high case in all periods except 2050–54, where they converge (222 vs 185).
- The market 5th (36 → 13) is far below the EIA-implied low case (89 → 57).
- Both match the author's prior expectation (high near-or-above EIA reference;
  low well below AEO low), with the high side exceeding it.
- Notable side finding: the market futures strip itself (67 → 53 real 2024$)
  sits ~25–50% BELOW the EIA-implied reference Brent (89 → 107) in every
  period. The model's reference fuel trajectory is well above what the market
  is currently willing to lock in, even during a war-premium episode.

Caveats for use: the 2035+ band is an extrapolation carried flat from the
last listed contract (Jan 2035); the 95th at long horizons is dominated by the
σ_long assumption (see sensitivities); quote date falls inside an active
geopolitical-risk episode, which raises the front of the futures curve and
front-tenor vols relative to a calm market.

# Press-sourced implied-volatility observations (pulled 2026-07-27 via WebFetch)

1. Reuters (syndicated at Yahoo Finance), "Analysis: Oil derivatives signal traders..."
   https://finance.yahoo.com/news/analysis-oil-derivatives-signal-traders-181111860.html
   Article date: 2026-03-06 (March 2026 escalation episode). Verbatim extracts:
   - "30-day at-the-money Brent implied volatility jumped 17.5 points to 68% over the past week"
   - "60- and 90-day tenors rose only 5.9 and 2.8 percentage points"
   - "The spread between the front-month Brent contract and the six-month contract widened to about $10"
   - "put-to-call ratio on West Texas Intermediate options roughly halved to 0.35"
   Used for: calibrating the tenor-decay rate of the war/event vol premium
   (premium ratio 5.9/17.5=0.34 at 60d, 2.8/17.5=0.16 at 90d => exponential
   decay constant k ~ 0.031-0.036 per day; we use 0.033/day).

2. Saxo Options Brief, 2026-07-20, "Oil vol at triple the VIX"
   https://www.home.saxo/en-sg/content/articles/options/options-brief---oil-vol-at-triple-the-vix---20-july-2026-20072026
   Verbatim extracts:
   - "OVX 60.02 (+7.35%), oil volatility at 3.20x the VIX"
   - "Brent rose as much as 3.8% to $91.42"; "Brent $90.26 (+2.45%)"; "WTI $83.64 (+2.27%)"
   Used for: corroborating the FRED OVXCLS level and the war-elevated front tenor.

3. Sharpe Two, "Forward Note", 2026-07-26
   https://sharpetwo.substack.com/p/forward-note-20260726
   Verbatim extracts:
   - implied volatility in oil reached the "high-60s this week"
   - USO realized vol spiked "above 90" during the Hormuz episode earlier in
     2026, cooled to "mid-40s", turning up again
   - "The futures term structure in oil (CL) is back in backwardation"
   Used for: corroboration of front-tenor IV level and regime.

GAP: no public, current (July 2026) quote for 12-month+ ATM Brent/WTI implied
vol was obtainable (Barchart/CME QuikStrike pages are JS-rendered; CME
settlement CSV timed out; ino.com unreachable; ICE EOD reports gated). The
long-tenor sigma is therefore a documented assumption anchored on the EIA STEO
probability workbook's calm-regime 10-month IV (26.8%, NYMEX data for the five
trading days ending 2025-09-04) plus the observed fast tenor-decay of event
premia above. See METHOD.md.

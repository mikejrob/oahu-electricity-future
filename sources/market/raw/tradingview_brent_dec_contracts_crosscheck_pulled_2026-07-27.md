# Cross-check: ICE Brent December contracts from TradingView
Source: https://www.tradingview.com/symbols/ICEEUR-BRN1!/contracts/ (ICE Futures Europe data)
Pulled via Claude Code WebFetch on 2026-07-27 (HST). Page state: "Market closed".

| Contract | Last-trade (expiry) date | Price | Change |
|----------|--------------------------|-------|--------|
| BRNZ2027 | 2027-10-29 | $74.57 | -2.11% |
| BRNZ2028 | 2028-10-31 | $72.35 | -1.59% |
| BRNZ2029 | 2029-10-31 | $71.32 | -1.21% |
| BRNZ2030 | 2030-10-31 | $70.72 | -0.91% |
| BRNZ2031 | 2031-10-31 | $70.13 | -0.71% |
| BRNZ2032 | 2032-10-29 | $69.57 | -0.34% |
| BRNZ2033 | 2033-10-31 | $68.73 | -0.15% |
| BRNZ2034 | 2034-10-31 | $68.02 | +0.01% |

Agreement with oilprice.com strip (same day): Dec2030-Dec2034 identical to the cent
(70.72, 70.13, 69.57, 68.73, 68.02); Dec2027-Dec2029 differ by $0.27-0.31
(intraday timing of "last" on the two aggregators). Confirms the far strip is a real
exchange settlement echo, not aggregator interpolation.
Note: ICE Brent futures for delivery month M cease trading at the end of month M-2
(e.g., Dec-2027 contract's last trade date is 2027-10-29). These last-trade dates are
used as T_i in the percentile construction.

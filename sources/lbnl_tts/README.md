# LBNL Tracking the Sun, 2024 edition

**What this is.** Lawrence Berkeley National Laboratory's *Tracking the
Sun* 2024 edition (data through 2023): the slide-deck report and the
executive summary (technical brief). Retrieved 2026-09-06 from
emp.lbl.gov (report: /sites/default/files/2024-10/Tracking%20the%20Sun%202024_Report.pdf;
summary: /sites/default/files/2024-08/Tracking%20the%20Sun%202024_Executive%20Summary.pdf).

**Files.**
- `LBNL_TrackingTheSun_2024_Report.pdf` — 46-page slide deck. sha256
  `4b08d2141a38f362ff80c52b65e318f9849ebcdb5ad961078f09e5a158878419`.
- `LBNL_TrackingTheSun_2024_ExecSummary.pdf` — technical brief. sha256
  `2c8f85111fa655e4a5e94c8f271efcd97130cbdbe19dd2dc3d8369ea0bf6c151`.

**Load-bearing points (verbatim or page-cited).**
- Installed-price sample definition (report p. 9): systems are removed
  if missing price data, third-party owned, **battery storage
  co-installed**, or self-installed. The headline price series is
  standalone, host-owned PV.
- Benchmark comparison (exec summary p. 4; report p. 32): "National
  median installed prices from the Tracking the Sun dataset are higher
  than a number of other common PV pricing benchmarks, which generally
  align more closely with the 20th percentile levels from Tracking the
  Sun. … a large portion of residential systems are loan-financed, and
  installed prices reported for these systems likely include dealer
  fees, adding anywhere from 5-50% to the total up-front price paid by
  the customer (typically not included in other benchmarks)."
- State-level residential median installed prices ranged $3.2–5.2/W in
  2023 (exec summary p. 5; report p. 37, states with ≥20 observations).
- State fixed effects in the pricing regression span roughly $2/W
  (report p. 42); battery storage is the largest modeled driver
  (+$1.4/W); system size moves prices −$0.7/W from the 20th to 80th
  size percentile.
- Hawaiʻi (report pp. 20, 46): the sample includes County of Honolulu
  data via Ohm Analytics, and "HI has, by far, the highest attachment
  rates of any state — virtually all new PV has storage." Because the
  installed-price sample excludes battery-co-installed systems, TTS's
  standalone price statistics carry essentially no Hawaiʻi market
  coverage.

**What it supports.** Report §2.3's residential-cost block: the
explanation of why TTS levels sit above quote-platform benchmarks
(EnergySage, Tesla, SolarReviews) and the use of TTS for dispersion
(state spreads) rather than levels.

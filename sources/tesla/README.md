# Tesla state-by-state residential solar pricing

**What this is.** Tesla's educational page "Solar Panel Cost Breakdown"
(tesla.com/learn/solar-panel-cost-breakdown) carries a table of "average
solar panel costs by state, for 8kW solar systems or larger, based on
Tesla Energy's internal data." It is the only single-vendor,
standardized, state-resolved residential price observation that includes
Hawaiʻi: LBNL *Tracking the Sun* has no Hawaiʻi residential sample, and
marketplace aggregators (EnergySage, SolarReviews) mix samples that
differ by market.

**Files.**
- `tesla_learn_solar-panel-cost-breakdown_wayback_20260614.html` — the
  only HTTP-200 Wayback capture (2026-06-14 06:51:10 UTC) of
  https://www.tesla.com/learn/solar-panel-cost-breakdown, retrieved
  2026-08-31 from
  http://web.archive.org/web/20260614065110/https://www.tesla.com/learn/solar-panel-cost-breakdown
  (includes Wayback toolbar chrome; the table is in the `<table>` element
  following the phrase "state-by-state differences in pricing").
  md5 9d26683a9ad027b8d4716367883acf28.
- `tesla_state_price_table.csv` — the table, transcribed verbatim.
  md5 39db1ee4f260a040e98c952ab866e002.

**The table** ($/W, 8 kW+ systems, Tesla Energy internal data):
AZ 2.54, FL 2.56, TX 2.67, CA 2.83, **HI 2.90**, NY 2.98, CT 3.01,
MA 3.45. Median of the eight sampled states 2.865; Hawaiʻi = 1.01x the
median, 1.02x California, 1.14x Arizona.

**What it supports.** Report §2.3's ranking sentence ("Hawaiʻi runs
slightly above California and below New York and Massachusetts") —
verified verbatim against this table. Because the table is restricted to
8 kW+ systems, it holds system size roughly fixed, isolating the
price-per-watt comparison from Hawaiʻi's smaller average system size.

**What it does not support.** The draft's earlier "about $2.27–2.82 per
watt nationally" range — this table runs 2.54–3.45. The page separately
quotes DOE's all-in benchmark at $2.74–3.30/W. Correct the range when
citing.

**Caveats.** The page is undated marketing/education content; internal
references ("In 2024, Tesla's permitting fees…") suggest 2024–25
authorship. Tesla wound down in-house installation from September 2024
in favor of certified installers who set their own prices; whether the
internal data reflect direct or certified-installer installs is not
stated. Live tesla.com returns HTTP 403 to automated fetches; all other
Wayback captures of this URL (2025-07 to 2025-12) are 403 pages. A
same-day screenshot of the live page would strengthen the observation
date; the June 2026 snapshot is the citable artifact.

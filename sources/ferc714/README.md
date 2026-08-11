# HECO (Oʻahu) hourly load, FERC Form 714

`heco_oahu_annual_load_2006_2024.csv` — annual average, peak, and net energy
for load, derived from FERC Form 714 Part III Schedule 2 (planning-area hourly
demand), respondent_id_ferc714 = 70 (Hawaiian Electric Company, Inc., EIA
19547, Oʻahu). Demand is **net of behind-the-meter distributed PV** (it is the
load the balancing authority serves).

Source: PUDL (Catalyst Cooperative) nightly build, table
`out_ferc714__hourly_planning_area_demand` (imputed/gap-filled series),
pulled 2026-07-24 from
https://s3.us-west-2.amazonaws.com/pudl.catalyst.coop/nightly/out_ferc714__hourly_planning_area_demand.parquet
PUDL currently ingests FERC 714 through calendar year 2024. Calendar-year 2025
(filed to FERC by mid-2026 as XBRL) is not yet in PUDL and would require
parsing the raw FERC XBRL filing.

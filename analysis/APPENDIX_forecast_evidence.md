# Appendix: HECO distributed-PV forecasts vs realized adoption (Oʻahu)

Data: `appendix_forecast_vs_actual.csv`; figure: `fig_heco_forecast_vs_actual.png`.
All series carry a `provenance` column; the two forecast series and the actuals are described below.

## Series

**PSIP 2016 (December).** Hawaiian Electric's 2016 Power Supply Improvement Plan Update
(PUC docket 2014-0183) projected Oʻahu cumulative distributed PV from 444 MW in 2016 to
896 MW in 2045. The series used here was digitized from a PSIP chart (decimal years snapped
to integer years). Digitization check: the series' 2016 starting value (444.0 MW) matches the
independently compiled installed base at end-2016 (440.9 MW) to within 0.7%.

**IGP "DER+BESS" series.** An on-disk extract labeled "IGP 2020" (working label in
`Compare_Loads.ipynb`; the citable current vintage is the 2023 IGP Final Report accepted by
the Commission in Decision & Order No. 40651, docket 2018-0165). Its units and scope are
unresolved: the series reads 1,115 MW in 2024, which exceeds Oʻahu-only distributed PV
(765 MW) by 1.46×. Its scale is consistent with an all-territories DER total and/or a PV-plus-
battery bundle; Hawaiian Electric's March 2025 communication cites a forecast of 1,186 MW of
cumulative distributed solar by 2030 (all territories), close to this series' 1,293 MW at 2030.
It is therefore shown separately and excluded from the Oʻahu headline comparison. On its own
terms the IGP-vintage forecast tracks recent adoption far more closely than the PSIP 2016
vintage: its implied 2024-level (1,115) is consistent with realized all-territories DER, and
its forward slope (2025-2035: 29.2 MW/yr) is between the PSIP slope and the realized rate.

**Actuals (Oʻahu).** Cumulative distributed PV from permit/interconnection records
(`der_points.parquet`, oahu-grid), year-end values, 2006-2024; 765.3 MW at end-2024 and
793.3 MW at mid-2025. External corroboration: Hawaiian Electric reports 61 MW of new private
rooftop solar added in 2024 across its territories (hawaiianelectric.com, "Hawaiian Electric
sees steady growth in solar installations", March 2025); the Oʻahu share implied by the
records used here is 44 MW, consistent with Oʻahu's roughly 70-75% share of territory-wide
additions. A transcription of Hawaiian Electric's quarterly installed-solar PDFs was not
available for this analysis (see caveats); the quarterly source exists at
hawaiianelectric.com/clean-energy-hawaii/our-clean-energy-portfolio/quarterly-installed-solar-data.

## Comparison

- Realized Oʻahu distributed PV reached **765 MW at end-2024**. The PSIP 2016 forecast does
  not reach that level until **2034 (770 MW)**. Adoption ran ten years ahead of the PSIP
  forecast within eight years of its publication.
- Over the forecast's own first eight years (2016-2024), PSIP projected additions of
  **27.1 MW/yr**; realized additions were **40.5 MW/yr** (1.5×).
- In the forecast's steady phase (2021-2045) PSIP projects **11.2 MW/yr**. Realized additions
  over 2020-2024 were **42.4 MW/yr** — 3.8× the projected rate for the same period, with no
  deceleration visible in the record (2024 additions: 44 MW Oʻahu).

## This report's trajectories

The three DistPV trajectories used in this report are shown on the same axes (operating
capacity, 30-year asset life, from `inputs_dgb`/`inputs_dgs`/`inputs_dga`
`gen_build_predetermined.csv`):

| trajectory | 2027 (MW) | 2050 operating (MW) | net rate 2027-2050 | gross build rate 2028-2050 |
|---|---|---|---|---|
| conservative | 800 | 1,000 | 8.7 MW/yr | 38.0 MW/yr |
| realistic | 820 | 1,560 | 32 MW/yr | 61.5 MW/yr |
| accelerated | 840 | 2,120 | 56 MW/yr | 85.0 MW/yr |

The accelerated trajectory is constructed as 2 × realistic − conservative (exact in the
inputs). Net rates are lower than gross build rates because the 2012-2016 build wave retires
within the horizon (30-year life). Placed against the record: the conservative trajectory's
gross build rate (38.0 MW/yr) approximately continues the realized 2020-2024 rate
(42.4 MW/yr); realistic assumes 1.5× the recent realized rate; accelerated assumes 2.0×.
On a net-of-retirements basis, the conservative trajectory (8.7 MW/yr) sits below the PSIP
2016 steady-phase rate (11.2 MW/yr) that realized adoption exceeded by 3.8×.

## Caveats

1. The PSIP series is digitized from a published chart, not transcribed from a table;
   snapped to integer years. Its 2016 anchor matches the realized installed base to 0.7%.
2. The IGP "DER+BESS" series' units/scope are unresolved (see above); it is not used in the
   Oʻahu headline comparison. Pinning it requires the IGP Final Report appendix tables
   (docket 2018-0165).
3. The actuals are compiled permit/interconnection records, not Hawaiian Electric's published
   quarterly series; the two agree on 2024 additions within the Oʻahu-share approximation,
   but a direct transcription of the quarterly PDFs would be the cleanest primary source and
   was not available on disk. System *counts* in the records (118k Oʻahu, end-2024) exceed
   Hawaiian Electric's reported active-system count (114k, all territories, end-2024),
   indicating the records count permits/events rather than active interconnections; the MW
   series, not the counts, is used here.
4. All capacities are cumulative installed MW-ac unless noted; the report trajectories are
   operating MW (net of 30-year retirements), which is why the conservative trajectory is
   nearly flat despite ongoing gross additions.
5. Web verification was limited to press-release-level numbers (PSIP 2045 mix shares, 2024
   additions, the 1,186 MW by-2030 forecast mention); the PSIP chart values themselves were
   not independently re-verified against the PSIP PDF tables.

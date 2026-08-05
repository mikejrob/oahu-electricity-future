# JERA part-load heat-rate derivation from EPA CEMS (issue #2)

The model's JERA blocks originally carried a fuel curve proportional to
output (6.92 MMBtu/MWh at every load, minimum load 30 of 125 MW), so the
plant paid no part-load penalty. This directory holds the empirical basis
for the replacement curve.

## Sources (all public)

- **EPA CEMS hourly emissions**, via the PUDL processed distribution:
  `s3://pudl.catalyst.coop/stable/core_epacems__hourly_emissions.parquet`
  (stable release marker `2026-07-14-1532-aadd5f4f3`; 4.87 GB, 1.009
  billion unit-hours — not vendored; fetch by URL). Columns used: gross
  load (MW), heat input (MMBtu), operating time, per CAMD unit-hour.
- **EPA–EIA crosswalk** (github.com/USEPA/camd-eia-crosswalk) and
  **EIA-860 generator attributes** via PUDL
  (`stable/core_epa__assn_eia_epacamd.parquet`,
  `stable/out_eia__yearly_generators.parquet`).

## Fleet selection (candidates.csv)

Documented criteria, no hand-picking: technology "Natural Gas Fired
Combined Cycle", prime mover CT, nameplate 140–260 MW (the F-class band —
excludes E-class below, G/H/J-class above), operating date 2002+, status
existing, CAMD match. 525 units at 215 mainland plants; 2022–2024 hourly
records extracted (13.8M unit-hours).

## Fit (unit_fits.csv; build/derive_jera_partload_from_cems.py)

Per unit: steady full operating hours only (both neighbor hours within
15% of the unit's realized max, ≥2,000 qualifying hours), weighted line
fit through binned medians of heat input vs gross load. 408 units at 181
plants survive. Fleet medians (IQR):

- realized full-load heat rate 6.895 (6.68–7.21) MMBtu/MWh — within 0.4%
  of the model's independently sourced 6.92 anchor;
- no-load fuel share alpha = 0.100 (0.05–0.17);
- realized minimum stable load 52% (45–58%) of max;
- part-load penalty +9.9% at 50% load, +3.7% at 75%.

A modern-vintage subset (2010+, n=90) is nearly identical (alpha 0.080,
min 51%, +8.8%/+3.4%), so the shape is not a vintage artifact.

## Applied curve (author-approved 2026-08-02)

Per 125 MW block, anchored at the sourced 6.92 full-load rate; minimum
load set at 50% — just below the fleet median 52%, within the IQR, and
unchallenged by JERA's proposal, which states no block-level turndown
figure (its flexibility claims rest on the simple-cycle portion, which
the model's four-block commitment already represents):

```
Oahu_JERA,62.5,.,.,476.0     # min 62.5 MW; 86.9 no-load + 6.225/MWh
Oahu_JERA,62.5,75.0,6.225,.
Oahu_JERA,75.0,100.0,6.225,.
Oahu_JERA,100.0,125.0,6.225,.
```

Average heat rates: 7.62 at minimum, 7.15 at 75%, 6.92 at full load.
Direction of effect: raises JERA-pathway fuel use and cost; the bias it
corrects was one-sided (report Section 4.2).

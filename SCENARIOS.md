# The scenario menu

Every scenario in this analysis, in plain language. The full menu solves
under two rooftop-solar trajectories (conservative and realistic), with a
core subset also solved under an accelerated trajectory and with rooftop
resources dispatched by the optimizer — over 500 solved configurations in all
(see the scenario map in the README). Each row is one solved optimization
(at 0.25% tolerance, refined to 0.1%); machine-readable
definitions are one line per scenario in `scenarios/*.txt`, and results are
aggregated in `results/RESULTS_SUMMARY.csv`.

**Naming:** `<config>_<oilpath>` with prefixes/suffixes for variants.
Oil paths, four cases (Appendix A.14): `refbrent` = EIA-anchored reference
(likely high; kept for comparability); `futbrent` = the Brent futures strip,
the market's central expectation; `lowbrent` / `highbrent` = the market 10th
and 90th percentiles from futures and option-implied volatility, real 2024$
via TIPS breakevens (quote date 2026-07-27). The former EIA AEO case spread
is archived (`*_aeo.csv`, `aeo_archive/`).
`_j120` = JERA capital at the vendor's +20% case. `_adv` = ATB *Advanced*
solar+battery basis. `lc_` = Class-C-only land screen.

## 1. The headline matrix (6 trajectories × 4 oil paths, 2 land screens)

| Config | Meaning |
|---|---|
| `C4_NOTHERMAL` | No new fuel-burning plant. Existing fleet + Puʻuloa + solar/storage/wind + Enhanced Geothermal (built in the base case under current-law credits). |
| `C1_LSFO250` / `C2_LSFO375` / `C3_LSFO500` | A modern combined-cycle plant on the existing low-sulfur fuel oil supply, at 250/375/500 MW. |
| `wb_C6_LNG500` | JERA's proposal alone: 500 MW combined cycle + FSRU + LNG tiers, 2030–2044. No Waiau. |
| `C5_LNG375` | The LNG configuration at the cost-minimizing 375 MW size. |
| `wr_C4_NOTHERMAL` | Waiau Repower forced, nothing else new. |
| `wr_C1_LSFO250`, `wr_C5/6...` | Waiau + the respective new plant. |
| `C6_STATUSQUO` | Waiau Repower **and** JERA LNG 500 together. The identifier is legacy and misleading twice over: this is **not** the status quo (the status quo builds neither), and it is not a plan any party has put forward — Hawaiian Electric has not endorsed the JERA proposal, and the two projects overlap in what they provide. The cell is a modeling bookend, the upper bound on new thermal capacity, not a proposal. |

All of the above solve at four oil paths (Appendix A.14) on the reference land screen —
agricultural/country-zoned land; Class A soils, golf courses, and road
buffers excluded; terrain admitted to 30% slope with graduated cost
premiums (0–15% at reference, 15–20% at +5%, 20–30% at +10%); prime B/C
capped at 10% per cluster; all D/E and non-ag admitted (27,256 eligible
acres; the current-law "S0" envelope in the companion land study,
github.com/mikejrob/solar-wind-landuse). The core subset repeats on the
Class-C-only screen (`lc_`).

## 2. JERA's capital range (`*_j120`, 22 cells)

Every LNG scenario re-solved with JERA's plant and import infrastructure at
their own +20% sensitivity (proposal p. 29), which restores the customs,
insurance, design-allowance and contingency their base estimate excludes
(p. 30). Reported results use the midpoint of base and +20%, with the band.

## Battery-ITC supplement (3 cells)

`bitcsched_*`: the current-law federal storage credit (48E — 30% for
construction beginning through 2033, zero after 2035) applied as battery
capital ×0.70 for 2027–2035 build vintages, full price after. Cells:
no-new-plant plus the JERA-500 bare/+20% pair, reference oil. Results:
no-new-plant −$0.62B; the JERA band turns fully positive (midpoint +$0.33).
Excluded from the baseline for conservatism (FEOC eligibility risk).

> *Naming note:* `C6_STATUSQUO` already includes the Waiau Repower, so the
> `wr_C6_*` cells are exact aliases of the corresponding `C6_STATUSQUO_*`
> cells (identical configurations; identical solutions). They are kept so
> every family carries the same trajectory labels.

## 3. Enhanced Geothermal (12 cells, plus 5 JERA-contingency variants)

`egs_{none,low,ref,high}` × {no LNG, LNG-500 forced}: Enhanced Geothermal blocked, or
priced at $6.2M / $10M / $14.7M per MW (2030, 2024$) — GeoVision optimistic /
documented compromise / ATB Conservative.

## 4. Solar-cost sensitivities

- `be_pv15_*` / `be_pv17_*`: solar+battery at 1.5× / 1.7× the baseline
  (≈1.8× / 2.0× the mainland ATB benchmark — near today's procurement-implied
  level), for the no-thermal, LSFO-plant, and JERA configurations.
- `*_adv` (86 cells): the full set on the ATB **Advanced** projection for
  both solar and battery — the sourced cheaper-renewables supplement.

## 5. Steelman and counterfactual cases

- `lngconv_*`: the import terminal with **existing plants converted** to burn
  LNG (Kalaeloa; plus Kahe 5/6 and CIP CT in the `heco` variant) and **no new
  plant** — tests whether the fuel benefit needs the plant. Conversion capex
  set to zero (upper bound; flagged).
- `norps_*`: the 2045 clean-energy mandate **removed** — the no-mandate
  baseline, the model's unconstrained choice (it builds 1,125 MW of gas), and
  forced JERA-500 at both capital cases.

## 6. Solve passes

Every cell solves cold at 0.25% MIP gap, then re-solves warm-started at 0.1%
(`outputs_p001_*`); the 0.1% value supersedes. Headline gaps between
scenarios are reported only when they exceed solver tolerance, and the report
flags any comparison inside it.

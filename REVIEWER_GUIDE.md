# Reviewer guide: the fastest paths to scrutinize this analysis

Written for technical reviewers — especially those who know the
Switch-Hawaiʻi lineage. The aim is that every load-bearing choice can be
checked quickly, from primary documents vendored in this repository, without
trusting any intermediate artifact. Findings can be sent privately (email the
authors) or publicly (GitHub issues); both are welcome and both get answered.

## In 15 minutes

```bash
git clone <repo> && cd <repo>
python verify_claims.py        # re-derives every headline input from vendored
                               # sources and hashes; exit 0 = all claims check
```
Then read `docs/CONVENTIONS.md` (the complete assumption set, ~5 pages) and
scan Table ES.1 in `report/` against `results/RESULTS_SUMMARY.csv`.

## In an hour: the weight-bearing judgment calls, one by one

Everything else is mechanical; these seven choices carry the results. Each row
says what we chose, where the evidence sits, and how to check it.

| # | Choice | What we did | Verify by |
|---|---|---|---|
| 1 | **Dollar unit & NPV date** | All inputs real 2024$; `base_financial_year=2027` used strictly as the discount anchor (not a dollar-year) | `docs/CONVENTIONS.md` §1; spot-check any input against its source ×CPI chain; `verify_claims.py` does this for the headline set |
| 2 | **Solar premium 1.20×** | Author floor on ATB 2024 Moderate; evidence from Honolulu retail + HECO PPA awards | Report §2.3; sensitivities at 1.5×/1.7× (`gen_build_costs_pv15/17`) and ATB-Advanced (`inputs_advsolar/`) bracket it both ways |
| 3 | **Battery co-location** | Derived from NREL's own PV-plus-battery hybrid: `(PVB−PV)/0.5` — interconnection saved + NREL's joint-install delta (~0.91–0.93 by year) | Recompute from `sources/ATBe_2024_v3.0.0_slice.csv` (PVB Class5 rows); compare the old flat 0.88 (2-hr GCC share) in `docs/CHANGES_FROM_WORKING_PAPER.md` |
| 4 | **JERA capital band** | Vendor bare-EPC ($3,020/kW, exclusions quoted) to vendor +20% (their own p.29 case); results reported at the midpoint with the band | `sources/JERA_Proposal…pdf` pp. 29–30, 35; public record (~$2B total, ~75% plant) cited in report §4.2 |
| 5 | **EGS cost trio 6/10/14.7** | Judgement call, documented: GeoVision low kept; $10M compromise reference; ATB-Conservative shape high | `docs/CONVENTIONS.md` EGS section; the option-value table in report §3 shows what turns on it |
| 6 | **Fuel prices** | R3 LSFO regression (slope 0.7388, 6.22 MMBtu/bbl) + contract-floor LNG + AEO2025 case spread, all real 2024$ | `build/build_brent_variants.py` (method disclosed inline); the published UHERO brief for the regressions |
| 7 | **LNG infrastructure, charged once** | FSRU/pipeline recovered via the fuel-tier fixed charge on activation; plant capital is plant-only | `switch_model.hawaii.fuel_markets_expansion` mechanics; tier `fixed_cost` in `inputs/fuel_supply_curves.csv`; no infra in `Oahu_JERA` capital |

## In one to two days: full reproduction

1. **Regenerate the inputs from ground truth**: `python
   build/build_corrected_inputs.py` — reads only `base_model/` (vendored) and
   `sources/` (hashed), and rebuilds `inputs/` byte-identically to what is
   committed.
2. **Re-solve any scenario**: `scenarios/` holds every cell's full definition
   (one line each — inputs dir, module flags, tolerances). Requires Switch
   2.0.9 + CPLEX; each cell is a single `switch solve-scenarios` call.
3. **Recompute any table/figure** from the per-scenario outputs feeding
   `results/`.

Scenarios will solve in minutes to a couple of hours at 0.25% tolerance, but 0.1% tolerances 
can take over 24 hours for some scenarios. To solve all of the scenarios would take a
considerable amount of time on a personal computer. On a larger server with many computing
cores, all scenarios can be solved simultaneously with complete results in one-to-two 
days.

## Solve quality

The current-law tax credits introduce a cost cliff that makes the credited
cases slower to solve and occasionally produces stuck (converged-but-wrong)
incumbents. `sanity_check_results.py` detects them; warm-starting from a
solved neighbor fixes them. Full detail: [`docs/SOLVER_NOTES.md`](docs/SOLVER_NOTES.md).

## Notes for readers of the Switch-Hawaiʻi lineage

Relative to the prior Switch-Hawaiʻi conventions, the deliberate deviations
are: (a) the dollar-unit/NPV-anchor split in row 1 (prior practice treated
`base_financial_year` as the dollar-year); (b) `ev_patched` = `hawaii.ev`
plus the one missing `Param` declaration; (c) `lng_conversion`'s
converted-plants list corrected to the actual generator names (the PSIP-era
entries had drifted and were inert); (d) battery cost from the ATB hybrid
rather than a flat co-location factor. Everything else follows the base
model's conventions, and the base model itself is vendored in `base_model/`
for line-by-line comparison.

## What we most want scrutinized

The premium (row 2), the JERA band (row 4), and the EGS trio (row 5) are the
three choices on which reasonable experts can differ; the report's results
are presented so that a reader who prefers different values can see exactly
what moves. If you check only one mechanical thing, make it row 7 — the
single-counting of the LNG import infrastructure — since it is where an
earlier version of this analysis went wrong in one direction and its
predecessor went wrong in the other.

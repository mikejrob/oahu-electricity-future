# External code audit — 5 September 2026

Audit target: commit `7ab98f9`, with the existing uncommitted edit to
`report/DRAFT_v7_full.md` left untouched. No model inputs, solver code,
published results, or report text were changed by this audit.

**Assessment: the added code contains two confirmed errors that affect the
committed model inputs, plus reproduction, validation, extraction, and
empirical-preprocessing defects. The
published quantitative conclusions need rechecking after corrected solves.**
This does not establish that the qualitative conclusions reverse.

## Scope and evidence

The public Git history begins with the first release, after the extensions
were already present. There is no pre-extension code commit against which to
diff everything. I treated `base_model/` as the trusted inherited input
boundary, reviewed the local model modules and the main added input,
scenario, extraction, and validation paths, and traced the principal
distributed-resource calculations. The continuation expanded review of the
empirical pipeline, plotting code, R explorer, and batch machinery. This is
a repository-wide, risk-based code audit, not an exhaustive line-by-line
certification or a fresh optimization validation. The inherited source is
treated as trusted; the questions concern the added transformations and how
they consume and present that source. External source documents were not
independently fact-checked.

Checks performed:

- All 84 Python files (82 original plus two audit scripts) parsed successfully; all 81 shell/SLURM
  scripts passed `bash -n`. These checks establish syntax only.
- `python3 verify_claims.py` passed. Its checks do not cover either of the
  principal defects below.
- Recalculated the conservative, trend, and accelerated committed net loads
  from the builder's equations: maximum discrepancy under 0.0000005 MW.
- Rebuilt reference inputs from the vendored base into a temporary directory,
  including the cost variants and fuel steps called by the main builder.
- Checked 902 first-pass scenario lines whose output names occur in the
  published summary: their input directories and aliased files exist.
- Confirmed 513 summary cells match the explorer's 513 matrix cells, alongside
  14 plan cells. This checks membership, not the correctness of their costs.
- `sanity_check_results.py` found missing raw outputs and checked zero
  dominance pairs. The checkout has no raw solver result directories; the
  default Python also lacks Switch and Pyomo. I did not instantiate or solve
  the full optimization model, reproduce regressions from missing parquet
  data, or execute the R application.

Reproduce the main numerical evidence without extra packages or changing
inputs:

```bash
python3 analysis/reproduce_code_audit.py
python3 analysis/reproduce_audit_continuation.py
```

The script emits JSON, including the battery energy totals, geothermal cost
rows, and rebuild differences. It intentionally reports evidence rather than
returning a blanket pass/fail certificate.

Continuation checks also matched all 513 summary costs to the explorer
within its rounding tolerance ($50,000, from 0.0001 billion), inspected the
complete R app source, and reproduced the quarantine and plan-layout bugs
using isolated fixtures and the actual affected Python functions. No raw
outputs were created in the repository. Details follow in findings 8–13.

## Confirmed findings, in priority order

### 1. P1 — Rooftop battery netting creates energy

Location: `build/build_netload_corrected.py:102–121`.

`BATT_DELIVER` is daily **MWh delivered per installed MWh**. Line 117 assigns
that energy times the evening weights directly to **MW**. Since the modeled
timepoints last two hours, integrating the two evening blocks delivers
twice the intended energy: 0.9076 rather than 0.4538 MWh/MWh/day.

Independently, lines 102–108 normalize charging over the entire period's
13 representative days. Each day discharges, but charging across all 13
days shares one daily allowance. Charging also needs the timepoint-duration
conversion. Unequal representative-day weights introduce a further mismatch
when these unweighted normalizations are annualized.

These equations reproduce the committed loads, so this is an active input
defect, not just an unused-script issue. Using the actual timeseries weights:

| 2050 rooftop family | Battery charge GWh/year | Battery discharge GWh/year | Net energy created GWh/year |
|---|---:|---:|---:|
| Conservative | 14.65 | 160.34 | 145.68 |
| Trend | 31.61 | 345.85 | 314.24 |
| Accelerated | 89.55 | 979.91 | 890.36 |

A battery with 86% round-trip efficiency must consume more energy than it
delivers. These are battery-only terms; PV is calculated separately. The
last column is the current unphysical contribution, not an estimate of the
change in optimal system cost.

Fix direction: express each daily charge/discharge allocation as energy,
normalize within each representative day, and divide by block duration when
writing MW. Assert daily and annual energy conservation and power/energy
limits. Decide explicitly how a low-sun day limits the assumed charge and
discharge. Rebuild all affected net-load families and plan quotas, then
re-solve. Because battery stock differs by rooftop trajectory, this error
does not cancel across trajectories. Even within one trajectory it can
change which investments and constraints bind. Reliability and reserve
findings also depend on the overstated evening demand reduction.

### 2. P1 — EGS cost sensitivities also remove battery credits

Location: `build/build_corrected_inputs.py:528–563`, with
`egs_variant()` at lines 484–502.

The low/high EGS variants are copied before the base table receives the
storage/geothermal capital-credit adjustment. `egs_variant()` credits the
EGS rows itself, but leaves battery rows at their uncredited values.

For the committed conservative inputs in 2030, bulk battery power capital
is $286,437.49/MW in the base file and $409,196.42/MW in both EGS variants;
energy capital is $221,736.00/MWh versus $316,765.71/MWh. Thus batteries
are approximately 42.9% more expensive in a supposedly EGS-only sensitivity.
The affected early build vintages are 2027, 2030, and 2035. There are 34
low/high EGS-named cells in the published matrix; trace their actual input
aliases when scheduling corrected runs. An analytically repriced result
using a different basis must be evaluated separately.

Fix direction: derive each EGS variant from the fully adjusted base table,
replace only EGS costs, and assert that every non-EGS row is identical.
Keep the EGS credit applied exactly once. This is a variant-construction
bug; it is not a judgment on the chosen tax-policy assumptions.

### 3. P1 — The documented rebuild restores superseded oil inputs

Location: `build/build_corrected_inputs.py:700–703` and `seed():332–340`.

The main builder still calls the older AEO-spread builder. It never calls
`build/market_band/apply_market_band.py`. Rebuilding reference inputs in
isolation changed all four low/high fuel files (including JERA-uplifted
versions). For example, 2050 low-case LSFO becomes $12.713254/MMBtu instead
of the committed market-case $8.081461/MMBtu.

The rebuild also omits `fuel_supply_curves_futbrent.csv`, its JERA variant,
the two AEO archive files, and `gen_info_egs100.csv`. Since `seed()` removes
the existing destination first, running the documented command in place
would remove those files. It prints successful verification nevertheless.

Fix direction: make one explicit build pipeline produce the current market
cases and all required variants, stage the result before replacing live
inputs, and compare the entire generated tree against a manifest. Do not
use the documented rebuild as a faithful reproduction until this is fixed.

### 4. P2 — The dominance gate does not check the published refinement basis

Location: `sanity_check_results.py:138–143,159–161`.

The broad sweep globs only `outputs_*` even in the default mode advertised
as `R010 > R0015 > outputs`. The earlier `cost()` function implements that
fallback, but the sweep bypasses it. A bad refined comparison can therefore
escape the gate even when the first-pass comparison passes. In addition,
the premium-pair test requires names starting with `be_pv15_`, whereas the
published families start with `nlv2b_`, `nlv2s_`, or `nlv2a_`.

Fix direction: share one scenario resolver with the report/explorer; parse
axes after removing the family prefix; require explicit coverage counts
against the published manifest. Test using synthetic good first-pass values
and inverted refined values. A zero-pair check must not be a successful
scientific validation.

The fixed $2 million sweep tolerance is also not "approximately twice"
a 0.25% gap for a multibillion-dollar objective. Use actual solver bounds
to distinguish uncertainty from a proven dominance violation. Claims that
larger forced plants must always be more expensive require additional
economic assumptions; they are not generic optimization identities.

### 5. P2 — Requested solver tolerances are reported as achieved gaps

Locations: `results/build_results_summary.py:48–56`,
`build/build_explorer_data.py:324–331`, and
`solve/promote_retries.py:25–57`.

The summary/explorer infer a gap from the directory prefix and presence of
`total_cost.txt`. They do not read termination status or a proven bound.
All 513 committed summary rows consequently say 0.001, despite the solve
documentation describing time-limited exceptions. The retry promoter also
writes a 0.1% confirmation marker without reading a bound.

A completed output file is not proof that the requested gap was reached.
The promoter's mathematical argument about a better incumbent is valid
only if the retry actually proves the claimed bound for the same model.
Without raw logs, I cannot establish the true gaps of individual cells.

Fix direction: retain incumbent, best bound, achieved gap, termination
reason, and input/code hashes in a per-solve manifest. Export requested and
achieved tolerances separately. Guard extractors against empty raw-output
trees; the summary builder currently replaces its CSV with a header-only
file on this checkout.

### 6. P2 — The empirical and market pipelines are not self-contained

Locations: `analysis/01_build_panel.py:28–30`, subsequent numbered analysis
scripts, and `build/market_band/build_market_percentiles.py:46` onward.

The panel builder depends on a historical temporary parquet path and an
external `oahu-grid` data file. Many analysis scripts hard-code the original
cluster directory. The market builder still generates a 5th/95th-percentile
product; the active application reads a separate 10th/90th JSON file that
this script does not write. There is no complete current rebuild chain
from the committed sources through these empirical/market inputs.

Fix direction: parameterize paths, provide source manifests or documented
retrieval steps, and make the selected percentile level an explicit shared
parameter. Archive superseded builders clearly. This does not by itself
show the committed parameter estimates are numerically wrong, but prevents
an independent end-to-end reproduction.

### 7. P2 — EGS capacity override cannot raise the input ceiling

Location: `model/egs_geothermal.py:112–126`.

The option is documented as allowing tighter or looser ceilings, but only
adds another upper-bound constraint. With the existing 100 MW input cap,
`--egs-max-capacity 150` still permits at most 100 MW. Also, checking
`GEN_BLD_YRS` skips capacity enforcement in periods without a new-build
option, even if an earlier plant remains operational.

Fix direction: override the underlying input parameter before its capacity
constraint is constructed, or document this as a tightening-only option.
Use operating-period membership for constraints on installed capacity.
This is a latent sensitivity-interface defect; no effect on the default
100 MW case was demonstrated here.

### 8. P2 — Stale-result quarantine also removes valid newer refinements

Location: `analysis/audit_stale_jera_refinements.py:43–54,69–71`.

Once the first-pass result is newer than the batch list, the script marks
**every** existing R010/R0015 result for that scenario stale. It never
checks the refinement's date or its input version. A newly completed,
correct refinement is therefore moved aside on the next `--quarantine`
run, and extractors fall back to the first-pass output. Repeating quarantine
can also collide with an existing `STALE_` destination.

Reproduction: a temporary tree with batch timestamp 1,000,000,000,
corrected first-pass timestamp 1,000,000,100, and newer refinement timestamp
1,000,000,200 still quarantines the refinement. The continuation script
executes the actual quarantine program to establish this.

Fix direction: identify stale results by input/code fingerprints, with
timestamps only as an explicitly limited fallback; preserve refinements
built on the corrected inputs. Make repeat quarantine collision-safe.
This is a demonstrated maintenance-path defect; raw results are absent,
so its historical effect on the published fleet is unknown.

### 9. P2 — The premium-layout plan chart ignores the selected quota design

Location: `analysis/plot_plan_price_tags.py:128–139`.

The family layout uses `for_design()`, but the premium layout calls
`point(template.format(...))` directly. Thus `--layout premium --design
hybrid` reads the unsuffixed, discarded floors-only plan cells. If those
exist it silently plots the wrong comparison; if only hybrid results exist
it omits the plan points. The continuation script executes this function
with a recording reader: all 12 plan reads ignore the requested design.

Separately, the plan plot and the two plan/methane assemblers still default
to `firmfloor`, while the active explorer selects `hybrid`. The explicit
design option works in those assemblers, but their documented default
commands do not reproduce the active report basis. Premium-layout titles
also say solar **and battery** change although `_pv_variant()` changes
utility solar capital and FOM only.

Fix direction: use a single current-design setting and the same scenario
resolver in both layouts and all assemblers. Test requested scenario IDs,
not only whether a figure was written. Whether an existing PNG used the
broken layout cannot be established from this checkout.

### 10. P2 — Explorer capacity charts label all thermal capacity as oil

Location: `build/build_explorer_data.py:498–504`; capacity view in
`explorer/app.R:339–363`.

The extractor splits thermal energy into Oil/LNG, but assigns the entire
thermal capacity to Oil and hard-codes LNG capacity to zero. All **897 LNG
rows** in the committed extract have zero MW. For the 500 MW JERA case in
2035, the explorer reports 2,121.95 GWh of LNG generation with **0 MW LNG**,
and **1,550.1 MW Oil**. The capacity tab presents these as technology
capacities without explaining that allocation.

Fix direction: retain a combined thermal-capacity category, or classify
plants by fuel capability with an explicit multi-fuel category. Do not
allocate installed capacity using annual fuel shares. Also preserve the
capacity when the Oil energy share is zero: the current conditional row
emission would otherwise drop it entirely. This is a presentation defect,
not evidence of a capacity error inside the solver.

### 11. P2 — The report's hourly reliability chart omits flexible loads

Location: `report/figures/make_report_figures.py:189–293`, `fig_reliability()`.

The demand line includes `zone_demand_mw` only, and the sole withdrawal
series is battery charging. EV charging and hydrogen production are not
read, although both are additional loads. The newer explorer explicitly
includes these terms. In the committed explorer extract for the identical
base scenario and sample days, EV charging is nonzero in all 24 blocks and
reaches **279.3 MW**. The report chart cannot explain that generation-demand
difference and can invite an incorrect reading of surplus/headroom.

Fix direction: derive both hourly displays from one balanced set of supply
and withdrawal components, clearly distinguish curtailed potential from
generation, and verify the residual per timepoint. Include hydrogen fuel
cell supply when present. The missing EV term is confirmed with committed
data; hydrogen's magnitude and the complete balance need raw outputs.

### 12. P2 — CEMS steady-operation filtering bridges outages and missing hours

Location: `build/derive_jera_partload_from_cems.py:55–68`.

The code first removes non-full-operation, zero-load, and zero-heat rows,
then uses `.shift(1)` and `.shift(-1)` on the remaining rows to check ramp
size. It does not check that timestamps differ by one hour. A retained
100 MW observation can therefore be considered steady between two similar
observations separated by an outage, startup, or missing-data interval.
That does not implement the stated requirement that both neighboring
hours be present and steady. This preprocessing feeds the JERA part-load
fit, an added transformation of the trusted source.

Fix direction: require consecutive, unique hourly timestamps on both
sides, with all three observations satisfying operating-quality criteria.
Then refit and compare retained counts, fleet-median no-load share, and
the resulting JERA curve. The selection defect is visible in the code;
its numerical effect cannot be determined without the CEMS parquet.

### 13. P3 — CEMS generator prints an invalid numeric heat-curve row

Location: `build/derive_jera_partload_from_cems.py:131–134`.

The segment-row formatter appends literal `.0` to each endpoint. The first
endpoint is already the float `62.5`, so the first proposed segment starts
`Oahu_JERA,62.5.0,75.0,...`. `62.5.0` cannot be parsed as a number. The
committed input rows and builder constants correctly use `62.5`, so this
affects reuse of the generated proposal, not the currently committed curve.

Fix direction: format both endpoints numerically, for example `{lo:g}`,
and round-trip the emitted rows through the input parser before suggesting
that they can be copied into `gen_inc_heat_rates.csv`.

## What the author should review line by line

Do these in order. Focus on the equations and the files actually consumed
by scenarios, rather than reviewing every duplicated generated CSV.

| Priority | Files | Questions that require your judgment |
|---|---|---|
| 1 | `build/build_netload_corrected.py`, `analysis/09_estimator2_firmed.py`, `analysis/10_wedge_paramz_firmed.py` | What does each estimated coefficient measure? Is the 24% wedge induced demand, losses, or a residual? Is battery behavior already included in the daytime PV response? Which daily energy and weather limits should the extrapolated schedule obey? |
| 2 | `build/build_corrected_inputs.py` | Trace each added generator's units, heat-rate intercepts, minimum load, outages, lifetime, reserves, connection costs, and credit treatment. Check the cost-row copy order and every sensitivity's non-target rows. |
| 2a | `build/derive_jera_partload_from_cems.py` | After repairing hourly adjacency, refit the curve. Assess whether combustion-turbine gross-output shapes transfer to the proposed combined-cycle plant's net output, and separate the selected 50% minimum-load assumption from the estimated no-load share. |
| 3 | `model/lng_conversion.py`, fuel supply CSVs, and the installed Switch `fuel_markets_expansion` implementation | Independently reconstruct one terminal's discounted fixed charges from activation and lifetime. Check late activation, mandatory shutdown, conversion scope, and the external $0.45B adjustment. Header comments about conversion costs differ from the extractor's statement that they are omitted. |
| 4 | `build/build_plan_quotas.py`, `build/build_igp_plan_tables.py`, `model/plan_mix_quota.py` | Match the published-plan categories and denominator, excluded must-run/Kalaeloa production, wind substitution, and hydrogen/biofuel treatment. Are the resulting constrained mixes the comparisons you intend? Recompute quotas after fixing loads. |
| 5 | `analysis/01_build_panel.py`, `analysis/08_rebuild_panel_hourshift.py`, `analysis/09_estimator2_firmed.py` | Verify geographic coverage, timestamp conventions, duplicate/missing hours, as-of installation joins, and the clock correction at year boundaries. Reconsider dropped standalone GHI controls, linear trends, serial correlation, and whether the regression supports causal language. These are methodological questions, not established coding bugs. |
| 6 | `build/market_band/`, `sources/market/METHOD.md` | Trace the exact active JSON back to the futures strip, volatility assumptions, inflation and period averaging. Decide what probability interpretation is intended for the log-symmetric band before assessing its formula. |
| 7 | `build/fig_reserve_cushion.py`, forced-outage pilot inputs, report reliability arithmetic | Separate deterministic reserve headroom from a probabilistic adequacy calculation. Inspect independent versus common-mode outages, weather sampling and storage state. Reassess the results after the evening-load correction. |
| 8 | `results/build_results_summary.py`, `build/build_explorer_data.py`, scenario/refinement scripts | For representative comparisons, trace the exact scenario definition, all input aliases, input hashes, achieved bounds, and the raw quantities entering each chart. Check thermal fuel-share approximations and capacity versus cumulative-build reporting. |

The added EV energy aggregation explicitly multiplies MW by timepoint
duration, and the pinned distributed-battery builder explicitly divides
energy by its two-hour blocks. Those are useful dimensional cross-checks
for the corrected net-load implementation, although they do not certify
the wider assumptions of either module.

### Additional judgment and interpretation checks

- **Rooftop wedge and storage accounting:** the daytime regression can
  already include battery charging's effect on grid load. Establish which
  part of that is in the 24% wedge before adding explicit charging again.
  Daily battery energy balance is necessary but does not settle this
  identification question. The fixed evening schedule also needs an
  explicit low-sun rule; fixing the two-hour conversion alone is incomplete.
- **Battery calibration:** `analysis/10_wedge_paramz_firmed.py` says the
  per-MWh regression coefficient is invariant to rescaling installed MWh.
  Algebraically it is the coefficient that rescales inversely; fitted total
  load response is invariant when the regressor is multiplied by a constant.
  Check the forecast's calibration and physical cap together. That script
  also prints “check PASSES” unconditionally rather than testing the cap.
- **Empirical confidence:** the active PV model replaces year fixed effects
  with a linear trend and omits standalone GHI. Check robustness to those
  choices and serial correlation before interpreting coefficients causally.
  The low-sun script's “PRIMARY” reliability paragraph combines the primary
  era coefficient with the secondary regression's GHI slope; its attribution
  should be corrected or the calculation kept within one specification.
- **Time horizon:** the six periods represent 28 service years, ending at
  2055, rather than 24 calendar years ending in 2050. The report explicitly
  acknowledges this near line 3260. Therefore the 3/5/5/5/5/5 weights are
  internally consistent, not an off-by-four arithmetic bug. Headings such
  as “2027–2050” should say these are investment-period labels.
- **Land and generation displays:** `solar_by_period()` is cumulative
  construction, not surviving operating capacity. No predetermined
  CentralTrackingPV rows were found in the current inputs, so an active
  retirement overcount was not established. Use `gen_cap.csv` for a land-in-use
  claim if future model revisions introduce retirements. Fuel-energy shares
  are a disclosed approximation for annual oil/LNG generation and emissions;
  they are not a suitable capacity allocation (finding 10).
- **Cross-tab costs:** the explorer's System costs tab can add $0.45B
  conversion capital, while Compare and All solves use the raw total. This
  is visible in code and partly disclosed in About, but the displayed cost
  basis should be stated on each tab. No additional cost-transfer defect was
  found in the 513 summary-to-explorer matches.

### Coverage and limits of the completed audit pass

| Area | Work completed | Remaining validation |
|---|---|---|
| Trusted base | Used as the inherited boundary; compared added transformations against it | No independent re-audit of inherited research or upstream Switch |
| Input construction | Cost formulas, credits, variant isolation, fuel rebuild, rooftop netting, and distributed/pinned resource builders | Corrected full rebuild and comparison of affected solves |
| Model extensions | Static review of added build restrictions, EGS interface, LNG conversion, EV addition, and hard/elastic plan quotas | Instantiate in the production Switch/Pyomo environment and inspect constraints |
| Scenario and solve lifecycle | Scenario references, refinement generation, promotion, staleness, quarantine, representative launchers; syntax across all launchers | Cluster execution, input hashes, solver statuses and objective bounds |
| Empirical analysis | Active regression/parameterization chain, timestamp alignment, radiation aggregation, CEMS fit, low-sun and geographic checks; targeted review of older alternatives | Raw parquet data and dependencies to reproduce estimates and sample coverage |
| Results and presentation | Summary/explorer consistency, complete R app source, report/plan plots, cumulative emissions and methane extraction | Raw dispatch and fuel outputs; R/browser rendering and scientific figure regeneration |
| Validation | Both evidence scripts, existing claim checker, syntax checks; result gate attempted | Result gate exits 1 with 39 missing cases and zero dominance pairs; it cannot validate the missing fleet |

No optimization, full empirical regression, browser execution, or cluster
job was performed. A clean syntax check or agreement between two derived
tables does not independently validate their common upstream results.

## Recommended next work

First fix the battery accounting, variant isolation, and rebuild pipeline;
add daily energy-balance and non-target-row identity checks. Then reproduce
a small comparison set: conservative/trend/accelerated no-new-plant;
matching JERA and conversion cases; and low/reference/high EGS on identical
battery costs. Inspect objective bounds and feasibility, and rebuild plan
quotas. Only then expand to the affected published fleet and regenerate
tables and figures. Preserve old outputs with their original input hashes
so the change in results can be explained rather than silently overwritten.

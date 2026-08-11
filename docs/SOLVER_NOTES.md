# Solver notes: the tax-credit cost cliff and how to solve around it

The current-law federal tax credits (48E, storage and geothermal) introduce
a class of solve-quality problems. A reviewer re-running the scenarios
should read this before trusting raw solver output on the credited cases.

## The cost cliff

Earlier versions of this model carried technology costs that decline
smoothly (the NREL ATB projections). The 48E credit adds a cliff: storage
and geothermal capital carry a 30% discount for build vintages through
2035, then jump back to full price in 2040 (`build/build_corrected_inputs.py`,
the `ITC48E` block; `docs/CONVENTIONS.md`):

```
battery $/MW:  ... 283,758 (2035)  ->  390,513 (2040, +38%)  -> decline
EGS $/MW:      ... 6,321,524 (2035) -> 8,810,479 (2040, +39%) -> decline
```

The cliff is economically correct — it drives the intended build-timing
pull-forward — but it has two solver consequences: slower solves across the
board (the flat-then-jump path weakens the LP relaxation; ~40 minutes per
cell at 0.25% against ~30 on smooth costs), and occasional stuck
incumbents — cells that cold-start into a poor integer solution, freeze
near a 0.95% gap, and report a **converged but suboptimal** result. Those
are the dangerous ones: the number looks final and is wrong.

## Detecting bad solves: `sanity_check_results.py`

Run after any solve, before trusting a number. It encodes relations that
must hold if the solves are correct and flags violations as stuck solves:

- **Monotonicity**: the LSFO ladder increases in plant size; the baseline
  increases with oil price; every Waiau bundle exceeds its Waiau-free twin.
- **Strict dominance**: for every pair differing in exactly one cost input
  made more expensive, the cheaper cell must cost no more (bare-EPC ≤ +20%
  capital; Advanced ≤ baseline; pv15 ≤ pv17).
- **EGS bang-bang**: EGS builds 0 or 100 MW, never in between.

It is also the hard gate in `push_both.sh`: no push while a solved result
violates a must-hold relation.

## Fixing bad solves: warm-start from the neighbor, not barrier

- **Barrier LP (`mipalg=4`) does not fix a stuck MIP.** The stall is a
  frozen branch-and-bound lower bound, not the LP; barrier on 8 cores
  still runs for hours.
- **Warm-start from a solved neighbor fixes it.** Each stuck cell differs
  from a clean cell by one cost input, so its optimal build is known: seed
  it as a CPLEX MIP start and the gap closes at the correct incumbent.
  `solve/barrier_resolve.py` (name is historical; it writes warm-start
  lines) reads flagged cells from the checker, seeds each from the right
  neighbor, and pins the EGS corner.

Standing recommendation: warm-start credited cells from the start. The
0.1% refinement pass already warm-starts each cell from its own 0.25%
solution (`scenarios/build_p001.py`), which is why it avoids these stalls.
The no-credit set (`results/RESULTS_SUMMARY_noitc.csv`) has smooth costs
and solved cleanly first pass — the difficulty is specific to the cliff.

## The integer-rejection loop

One cell (`nlv2s_be_pv15_C6_STATUSQUO_lowbrent`) repeatedly logged
"Integer feasible solution rejected — infeasible on original model" and
froze far from the target gap: the presolved model accepted candidates
that violate original-model constraints by more than the default 1e-6
feasibility tolerance, so every candidate was discarded on lifting.
Warm-starting and disabling scaling did not cure it; **loosening the
feasibility tolerance to 1e-4** did (solved to 0.23%, objective within
0.03% of the value reconstructed from its earlier dispatch output; basis
condition number ~1e17, consistent with tolerance as the binding issue).
If another cell loops on rejected incumbents, apply the same option first.

## EGS sensitivity is analytical, not a full-MIP solve

On the credited basis a subset of the EGS cost-sensitivity cells return an
objective inconsistent with their own build: the warm-start loads C4's
exact build, yet the cell reports a higher cost than C4 despite cheaper
EGS — impossible, and re-solving does not reliably fix it. The resolution:
the EGS sensitivity needs no re-optimization. EGS is bang-bang (0 or
100 MW) and, when built, sits at its cap with dispatch unchanged, so the
sensitivity is a **capital reprice** off two clean base cells:

- skip corner = `egs_none` (the `no_egs` module);
- built corner = `egs_ref` (= `C4_NOTHERMAL`), shifted at any other EGS
  price *p* by `EGS_capital_NPV × (p/ref − 1)` (reprice constant from the
  clean `_adv` cells: ref→low saving 0.42 ± 0.02 B);
- reported value = `min(skip, built corner)`; EGS builds iff the built
  corner is cheaper.

At reference oil: high cost → skip (27.30, 0 MW); ref → build (26.72,
$0.58B saving); low → build (~26.30, ~$1.0B). Report EGS numbers are
derived this way; `sanity_check_results.py` treats these cells as
optional.

## "infeasible" in a worker log is usually not a failed cell

`switch_model.hawaii.smooth_dispatch` runs a second solve to smooth
dispatch among equal-cost options. When that pass fails, Switch prints

    WARNING: model became infeasible when smoothing; reverting to original solution.

and writes the original solution normally — cost, capacity, and emissions
are unaffected. Two things invite misreading: a worker log holds many
scenarios, so the `--scenario-name` at the top is not the cell that
printed the message; and `--suffixes iis` makes CPLEX grind out an empty
IIS on any infeasible solve. To separate real failures from smoothing
reverts:

    awk '/^running scenario /{ if(cur && bad && !rev) print "FATAL " cur; cur=$3; bad=0; rev=0; next }
         /^ *0 *0 *infeasible/{ bad=1 }
         /reverting to original solution/{ rev=1 }
         END{ if(cur && bad && !rev) print "FATAL " cur }' logs/<log>.out

A cell is genuinely dead only when no solution is written — confirm
against output freshness, never against the job's exit code.

## The hard cells

Scenarios that stall near 0.1% on the credited basis are listed in
[`HARD_CELLS.md`](HARD_CELLS.md) with the looser-gap / retry workflow.

## The fuel-alias bug (August 2026)

The `be_pv15`/`be_pv17` `wb_C6_LNG500` `*_j120` cells on the market
low/futures/high oil paths pointed at the reference-oil jera120 fuel
curve — a copied `--input-alias` in four scenario lists — making a
+20%-capital cell cheaper than its bare-capital twin, an impossibility.
The dominance sweep caught it. The six cells were quarantined
(`STALE_MISFUEL_*`) and re-solved on the per-path curves
(`inputs/fuel_supply_curves_<path>_jera120.csv`; 24 fixed lines across
four lists); after the re-solve every `_j120` cell sits above its bare
twin on all four paths. No report figure used the affected cells; they
appeared only in the explorer's Costs-tab band at those solar tiers and
in six RESULTS_SUMMARY rows, both rebuilt. Disclosed as public issue #8
while in progress; this note is the record of the fix, and it is why the
dominance sweep is a hard push gate.

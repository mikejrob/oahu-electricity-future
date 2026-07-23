# Solver notes: the tax-credit cost cliff and how to solve around it

This file documents a class of solve-quality problems introduced when the
model adopted the current-law federal tax credits (48E, for storage and
geothermal), and the tools that detect and fix them. A reviewer re-running
the scenarios should read this before trusting raw solver output on the
credited cases.

## What changed, and why it made the model harder

Every prior version of this model carried technology costs that decline
**smoothly** across the horizon (the NREL ATB projections). The current-law
48E credit adds a **cost cliff**: storage and geothermal capital carry a 30%
discount for build vintages through 2035, then jump back to full price in
2040 (see `build/build_corrected_inputs.py`, the `ITC48E` block, and
`docs/CONVENTIONS.md`). The credited path is:

```
battery $/MW:  ... 283,758 (2035)  ->  390,513 (2040, +38%)  -> decline
EGS $/MW:      ... 6,321,524 (2035) -> 8,810,479 (2040, +39%) -> decline
```

The cliff is economically correct — it is the whole point of an expiring
credit, and it drives the intended build-timing pull-forward (capacity moves
into 2027–2035 to capture the credit). But it has two solver consequences:

1. **Slower solves across the board.** The flat-then-jump cost path weakens
   the LP relaxation (many build-timing plans tie in cost), so every cell
   takes roughly 40 minutes at 0.25% tolerance, up from ~30 minutes on the
   smooth-cost model. This is normal and expected; the main run completed all
   184 cells at this pace.

2. **Occasional stuck incumbents.** A minority of cells (the EGS
   cost-sensitivity cells) cold-started into a poor integer incumbent and
   froze at a ~0.95% MIP gap, then reported a **converged but suboptimal**
   result. These are the dangerous ones: the number looks final but is wrong.

## Detecting bad solves: `sanity_check_results.py`

Run after any solve, before trusting a number:

```
python sanity_check_results.py            # 0.25% pass (outputs_)
python sanity_check_results.py --p001     # 0.1% pass (outputs_p001_)
```

It encodes relationships that must hold if the solves are correct, and flags
any violation as a stuck/suboptimal solve rather than a real result:

- **Monotonicity**: the LSFO ladder increases in plant size; the baseline
  increases with oil price; every Waiau bundle exceeds its Waiau-free twin.
- **Strict dominance sweep**: for every pair that differs in exactly one cost
  input made more expensive, the cheaper cell must cost no more. This covers
  bare-EPC ≤ +20% capital, Advanced-renewables ≤ baseline, and pv15 ≤ pv17 —
  ~170 pairs across ~300 cells. A single inversion means the "cheaper" cell
  over-solved (stuck).
- **EGS bang-bang**: EGS builds 0 or 100 MW, never in between. The checker
  reports the value at each cost level (`egs_none − forced-100`) and confirms
  the pinned build is the corner it should be.

In this build the sweep found exactly **one** genuinely stuck cell out of
~300 — the check does its job of isolating the rare bad solve without
re-solving everything.

## Fixing bad solves: warm-start from the neighbor, not barrier

Two fixes were tried. Only the second works.

- **Barrier LP (`mipalg=4`) does NOT fix it.** The stall is in MIP
  branch-and-bound (a frozen lower bound at ~0.95% gap), not in the LP, so
  switching the root LP from dual simplex to barrier — even on 8 cores — still
  runs for hours. Cores help barrier's factorization but not this bottleneck.
  Do not reach for barrier here.

- **Warm-start from a solved neighbor fixes it.** Each stuck cell differs from
  a clean cell by exactly one cost input, so its optimal build is known: seed
  it as a CPLEX MIP start and the root gap closes at the correct incumbent.
  Use the bang-bang corner to pick the seed:
  - `egs_low_*` (cheap EGS → builds 100 MW): seed from the built-100 base
    (`C4_NOTHERMAL_<oil>` for no-LNG, `egs_ref_lng_forced_*` for forced-LNG).
  - `egs_high_*` (expensive EGS → skips): seed from the 0-EGS base
    (`egs_none_*`, generated with the `no_egs` module).

  The driver is `solve/barrier_resolve.py` (name is historical; it now writes
  warm-start lines). It reads flagged cells from `sanity_check_results.py` or
  takes explicit names, seeds each from the right neighbor, and pins the EGS
  corner. The scenario lists it produced are `scenarios/scenarios_egs*_ws.txt`.

## Standing recommendation

Warm-start credited cells from the start rather than cold-starting them. The
0.1% refinement pass already warm-starts each cell from its own 0.25%
solution (`scenarios/build_p001.py`), which is why the refinement pass does
not hit these stalls. For any fresh re-solve of the 0.25% pass on the credited
basis, seed the EGS cost-sensitivity cells from their neighbors up front, or
expect to clean up a handful afterward with the driver above.

The no-credit sensitivity set (`results/RESULTS_SUMMARY_noitc.csv`) has smooth
costs and none of these problems — it solved cleanly on the first pass. The
difficulty is specific to the cost cliff the credit introduces.

## Update: EGS sensitivity is analytical, not a full-MIP solve

Further investigation showed the EGS cost-sensitivity cells (`egs_low_*`,
`egs_high_*`) are not just slow — on the ITC basis a subset return an
**objective inconsistent with their own build**: the warm-start loads C4's
exact build (verified: EGS=100 MW, solar=5,105 MW, identical), yet the cell
reports a higher cost than C4 despite cheaper EGS. An identical build with a
cheaper input cannot cost more. This is a solver pathology specific to the
cliff-degenerate cases, and re-solving does not reliably fix it.

The resolution is to recognize that the EGS sensitivity does not require a
re-optimization at all. EGS is bang-bang (0 or 100 MW) and, when built, sits
at its resource cap with capital sunk and dispatch unchanged, so the rest of
the system (solar, storage, dispatch, emissions) is identical across EGS cost
levels. The sensitivity is therefore a **capital reprice** off two clean base
cells:

- **EGS off / skip corner** = `egs_none` (the `no_egs` module; solves cleanly).
- **EGS built corner** = `egs_ref` (= `C4_NOTHERMAL`; solves cleanly, builds
  100 MW).
- At any other EGS price *p*, the built-corner cost = `egs_ref` shifted by the
  EGS capital reprice `EGS_capital_NPV x (p/ref - 1)`. The reprice constant is
  extracted from the clean `_adv` cells (which solve correctly): the ref->low
  saving is 0.42 +/- 0.02 B.
- The reported cell value = `min(skip, built-corner)`; EGS builds iff the
  built corner is cheaper.

At reference oil this gives: EGS off 27.30; at high cost the built corner
exceeds the skip, so the model skips (cost = 27.30, 0 MW, $0 saving); at ref
cost it builds (26.72, 100 MW, $0.58 saving); at low cost it builds
(~26.30, 100 MW, ~$1.0 saving). Report EGS numbers are derived this way, not
from the pathological full-MIP cells. `sanity_check_results.py` treats the EGS
sensitivity as derived.

## The specific hard cells

The scenarios that stall near 0.1% on the ITC basis are listed in
[`HARD_CELLS.md`](HARD_CELLS.md), with the looser-gap / retry workflow.

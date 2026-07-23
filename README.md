# Oʻahu's Electricity Future

An open, reproducible analysis of what Hawaiian Electric and Hawaiʻi should
build to keep Oʻahu's lights on through 2050 — solar-procurement reform,
Enhanced Geothermal, the Waiau Repower, and the JERA LNG proposal — using the
same class of capacity-expansion model utilities and regulators use to plan
decades of investment.

> ⚠️ **Pre-release.** This analysis is published for public scrutiny and
> comment before being finalized. Numbers may be refined during the comment
> period (see [`COMMENT_POLICY.md`](COMMENT_POLICY.md)); cite by release tag.

## What the analysis finds

1. **Cheaper solar-and-storage deployment is the biggest lever on Hawaiʻi's
   electricity costs** — worth several times any fuel decision studied here.
   The Hawaiʻi cost premium sits in procurement, permitting, and
   interconnection — processes policy can fix; hardware, labor, and land
   price near mainland benchmarks.
2. **Building the JERA LNG bundle costs modestly more than building no new
   fuel plant** — about $0.54 billion at reference oil (roughly two-tenths of
   a cent per kilowatt-hour), and more in every oil-price case. The gap is
   small, so contract structure, timing of the clean transition, upstream
   emissions, and risk carry the decision — and they point the same way as
   the cost.
3. **Some results are not close**: the Waiau Repower raises system cost by
   ~$1.4 billion under every assumption tested; a right-sized plant beats an
   oversized one; and, under current federal law, Enhanced Geothermal is in
   the least-cost build.
4. **Land is a question of timing**: every pathway that honors the 2045
   clean-energy mandate — including JERA's — builds nearly the same solar on
   nearly the same land, differing mainly in when it gets built.

The full findings, methods, and caveats are in the report
([`report/`](report/)); every number traces to a vendored public source.

## The scenario set

**184 scenario solutions** on a **current-law base case** — the federal
storage and geothermal tax credits (48E) that survive the 2025 budget
reconciliation act are in force, with a no-credit sensitivity reported
alongside. Across two solve tolerances: the headline matrix
(six thermal trajectories × three oil-price paths, on two land screens), the
EGS cost cases, solar-cost sensitivities from the ATB *Advanced* projection
to twice-mainland premiums, JERA's full capital range, LNG-conversion and
no-new-plant configurations, and the no-mandate counterfactuals.
[`SCENARIOS.md`](SCENARIOS.md) is the menu; results are in
[`results/`](results/).

## Check the work

```bash
python verify_claims.py   # re-derives every headline input from the vendored,
                          # hashed sources on a bare clone; exit 0 = verified
```

- **15 minutes to half a day**: [`REVIEWER_GUIDE.md`](REVIEWER_GUIDE.md)
  gives tiered paths to scrutinize every load-bearing choice.
- **Questions**: [`FAQ.md`](FAQ.md). **Comments**:
  [`COMMENT_POLICY.md`](COMMENT_POLICY.md) — public issues or private email,
  both answered.
- **Assumptions**: [`docs/CONVENTIONS.md`](docs/CONVENTIONS.md), one page per
  choice, with sources.
- **Re-solving**: any single scenario solves on an ordinary 4-core machine
  in well under 6 GB of memory — typically under an hour at the 0.25%
  tolerance, though refining to 0.1% has a heavy tail (a few cells exceed
  24 hours). Solving all 184 scenarios at both tolerances is ~2,500–3,000
  core-hours — a batch-computing task; [`solve/README.md`](solve/README.md)
  details the requirements, timings, and scripts.

## Layout

```
report/          the report and figures
base_model/      the underlying Oʻahu grid model (Ethan Hartley), vendored
build/           scripts that regenerate all inputs from base_model/ + sources/
inputs*/         the generated model inputs (byte-reproducible)
sources/         vendored primary documents, hashed and verified
scenarios/       every scenario's complete definition (one line each)
solve/           SLURM solve scripts (Switch 2.0.9 + CPLEX)
results/         solved results
docs/            conventions, corrections, analyses
```

## Relationship to earlier work

This analysis supersedes a 2026 working paper by the same authors — a
withdrawn report we regret having released too early. Errors in
that paper were corrected here, and the analysis was substantially extended;
[`docs/CORRECTIONS.md`](docs/CORRECTIONS.md) documents both, item by item,
with direction of effect. The base grid model was developed by Ethan Hartley,
building on Matthias Fripp's open-source Switch platform and Switch-Hawaiʻi
work. It also connects to a paper published by Imelda, Matthias Fripp, and 
Michael Roberts in AEJ-Policy in 2024, "Real Time Pricing and the Cost of 
Clean Power". (https://www.aeaweb.org/articles?id=10.1257/pol.20220506)

## What comes next

[`V2.md`](V2.md): the planned second edition, centered on a **regional
(nodal) model of the Oʻahu grid** — transmission, distributed-resource
locational value, and renewable-energy zones — plus the refinements queued
from this edition. Suggestions welcome via issues.

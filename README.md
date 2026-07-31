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

## Versions

> **Changed in pre-v1.02:** the oil-price cases are now four: the EIA-anchored
> reference (kept, and documented as likely high), the **Brent futures strip**
> as a market central case (`futbrent`), and the **market 10th/90th
> percentiles** (`lowbrent`/`highbrent`) from futures and option-implied
> volatility, deflated on TIPS breakevens (quote date 2026-07-27; full method
> and data in `sources/market/`, report Appendix A.14). The former EIA AEO
> case spread is archived (`*_aeo.csv`, `aeo_archive/`).

- **pre-v1.01 (current)** — this release: the single-node model with
  corrected distributed solar and storage (report Appendices A.11–A.13),
  three rooftop trajectories, four oil-price paths, over 500 configurations solved. **Open for
  comment: we ask that comments and suggestions arrive by September 1,
  2026** (tentative; this line is the authoritative date). Pre-release
  updates increment as pre-v1.02, pre-v1.03, …
- **v1 (planned)** — the locked version of record, after the comment
  period, our responses, and revisions. Post-lock changes will be limited
  to documented errata; new suggestions will be directed to v2.
- **v2 (planned)** — the regional (zonal) grid model described in `V2.md`.
- An earlier working paper, since withdrawn, preceded this series
  (corrections in `docs/CORRECTIONS.md`).

## The scenario set

**over 500 solved configurations** on a **current-law base case** — the federal
storage and geothermal credits (48E) that survive the 2025 budget act, with
a no-credit sensitivity alongside. The space has six axes:

| Axis | Options |
|---|---|
| New thermal plant | none / LSFO 250–375–500 MW / LNG 375 / JERA LNG 500 (bare-EPC and +20% capital) / Waiau Repower bundles / both projects together (Waiau + JERA 500) |
| LNG use | none / new plant / conversions of existing plants (Kalaeloa alone, or + Kahe 5–6 + CIP) |
| Oil price | four paths: market 10th percentile / Brent futures / EIA-anchored reference / market 90th percentile (Appendix A.14) |
| Solar & battery cost | ATB Moderate +20% Hawaiʻi premium (base) / ATB Advanced / 1.5× and 1.7× stress cases |
| Land screen | reference (graduated slope to 30%) / Class-C-constrained |
| Rooftop trajectory | conservative (~1,000 MW by 2050) / realistic (~1,560) / accelerated (~2,120, core subset) |

Plus Enhanced Geothermal cost/availability variants, no-mandate (RPS
removed) counterfactuals, and a core subset re-solved with rooftop resources
dispatched by the optimizer instead of netted from demand. The full menu solves under both the conservative and realistic rooftop
trajectories at each oil path; every solve reaches 0.25 percent optimality
tolerance and is refined to 0.1 percent.

One figure summarizes the space — every comparable solve, by family and
rooftop trajectory:

![All solved scenarios](report/figures/fig_scenario_map.png)

Three readings from the map: the conversion configurations sit left of the
no-new-plant baseline (the only LNG configurations that do); every
new-plant family sits right of it; and within each family the realistic
rooftop trajectory (green) sits left of the conservative one (blue) —
rooftop growth lowers system cost across the board.

## Pre-lock corrections

Known items queued for correction before the v1 lock (planned after the
comment window closes) are tracked as GitHub issues labeled
**`pre-v1-lock`** on this repository — that issue list is the
authoritative punch list. Post-lock changes will be limited to documented
errata.

## Explore the results interactively

Every solved scenario — system costs, generation mixes, emissions, and
sample-day hourly dispatch — can be browsed at
**https://mikejrob.github.io/oahu-electricity-future/** (runs entirely in
the browser; first load takes a moment). The app and its data extracts live
in [`explorer/`](explorer/); `build/build_explorer_data.py` regenerates the
extracts from the solve fleet.

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
  24 hours). Solving the full set of configurations at both tolerances is ~6,000–7,000
  core-hours — a batch-computing task; [`solve/README.md`](solve/README.md)
  details the requirements, timings, and scripts. It's best to use just one
  core if using the University of Hawai‘i HPC becasue extra cores do little
  to improve solve time and will greatly reduce CPU utilization. We used
  CPLEX to solve. Open source solvers will require more computing time.

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
building on Matthias Fripp's open-source Switch platform and [Switch-Hawaiʻi
work](https://github.com/switch-hawaii/ulupono_scenario_2.1). It also connects 
to a paper published by Imelda, Matthias Fripp, and Michael Roberts in AEJ-Policy 
in 2024, "Real Time Pricing and the Cost of Clean Power". 
[https://www.aeaweb.org/articles?id=10.1257/pol.20220506](https://www.aeaweb.org/articles?id=10.1257/pol.20220506)

## License and attribution

Code in this repository is licensed under the **Apache License, Version
2.0** ([`LICENSE`](LICENSE)), matching the license of the Switch model it
builds on; see [`NOTICE`](NOTICE) for attribution and for the files
derived from Switch. The report text and figures are offered under
**CC BY 4.0** — quote, adapt, and republish them with attribution.
Vendored third-party data under `sources/` remains subject to its
publishers' terms ([`SOURCES.md`](SOURCES.md)).

## What comes next

[`V2.md`](V2.md): the planned second edition, centered on a **regional
(nodal) model of the Oʻahu grid** — transmission, distributed-resource
locational value, and renewable-energy zones — plus the refinements queued
from this edition. Suggestions welcome via issues.

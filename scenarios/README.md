# Scenario definitions

Each `.txt` file lists complete, one-line-per-scenario definitions: scenario
name, input directory, any input-file aliases (cost or fuel variants), the
force/block modules that define the configuration, and solver tolerances. Any
line can be run standalone with `switch solve-scenarios`. `SCENARIOS.md` at
the repository root describes every scenario in plain language.

## The four-path market fleets (current)

The current fleet solves every configuration on the four market oil paths
(market 10th percentile / Brent futures / EIA reference / market 90th
percentile; report Appendix A.14). The lists:

| File | What it covers |
|---|---|
| `market_lh_b.txt` / `market_lh_s.txt` | The core matrix re-solved at the market 10th/90th paths (base and trend rooftop) |
| `market_fut_b.txt` / `market_fut_s.txt` | The Brent-futures central path |
| `netload_v2b.txt` / `netload_v2s.txt` | The corrected distributed-solar families (all four paths) |
| `j120fix_b.txt` / `j120fix_s.txt` | JERA +20% capital at the market paths |
| `solarmult_oil.txt` | Solar-premium cases (1.5x/1.7x) crossed with oil paths and conversions |
| `matrix_nlv2s.txt` | The trend-rooftop oil x solar matrix behind report Figure 4.3 |
| `norps_conv.txt` / `norps_conv_jera.txt` | No-mandate conversions and optional-JERA cells |
| `refine_matrix_key.txt` / `rescue_stuck2.txt` | 0.1% refinements and numerically-stuck re-solves |

## The 0.25% (first-pass) lists (original generation; AEO-era)

| File | Cells | What it covers |
|---|---:|---|
| `scenarios_p025_reference.txt` | 46 | Headline matrix on the reference land screen: six thermal trajectories × the original three-path AEO oil spread (superseded by the four market paths; see the market fleets below), the EGS cases, the solar-premium break-evens |
| `scenarios_p025_lc.txt` | 18 | The same core configurations on the Class-C-only land screen |
| `scenarios_p025_jera120.txt` | 22 | Every JERA scenario re-solved at JERA's +20% capital case (the top of the reported band) |
| `scenarios_p025_advsolar.txt` | 86 | The full set on the ATB *Advanced* solar+battery basis (the cheaper-renewables supplement) |
| `scenarios_norps.txt` | 4 | The no-clean-energy-mandate cases (Section 4.8) |
| `scenarios_lngconv.txt` / `scenarios_lngconv_heco.txt` | 3 + 1 | LNG-conversion cases: FSRU + existing-plant conversions with no new plant (Section 4.7) |
| `scenarios_pvjera.txt` | 4 | JERA at the 1.5×/1.7× solar-premium levels (both capital cases) |
| `scenarios_p025.txt` | 64 | Informational combined copy of the reference + lc core |

## The 0.1% (refinement) pass

`build_p001.py` regenerates `scenarios_p001_ready.txt` (untracked; generated)
from all lists above: every cell with a finished 0.25% solution and no 0.1%
solution yet, warm-started from its own first-pass result (`mipstart`),
tightened to 0.1%, writing to `outputs_p001_<name>/`. Idempotent — rerun any
time; `solve/p001_topup.slurm` does so automatically when the refinement
arrays drain. Final results use the 0.1% value wherever it exists.

## Generators

- `build_scenarios.py` — produces the core reference/lc lists from the
  scenario menu (names, configurations, tolerances).
- `build_p001.py` — produces the refinement list as above.
- The supplement lists (`jera120`, `advsolar`, `norps`, `lngconv*`, `pvjera`)
  were generated from the core lists by the documented transformations in the
  repository history and are committed as data; each line is self-describing.

## Naming note: "nlv2" is not the v2 model

Scenario lists `netload_v2b.txt`/`netload_v2s.txt` and directory prefixes
`inputs_nlv2*`, `outputs_nlv2*` (with `dgb/dgs/dga` for the dispatched-generator
variants and `R010_`/`R0015_` for gap refinements) belong to the corrected
distributed-solar treatment (v1 as first circulated let rooftop PV retire to
zero by 2050; fixed since pre-v1.01). "v2" is reserved for the regional (nodal)
grid model described in `V2.md`. The prefixes are frozen because solve
fleets and refinement machinery reference them.

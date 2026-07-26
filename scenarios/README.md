# Scenario definitions

Each `.txt` file lists complete, one-line-per-scenario definitions: scenario
name, input directory, any input-file aliases (cost or fuel variants), the
force/block modules that define the configuration, and solver tolerances. Any
line can be run standalone with `switch solve-scenarios`. `SCENARIOS.md` at
the repository root describes every scenario in plain language.

## The 0.25% (first-pass) lists

| File | Cells | What it covers |
|---|---:|---|
| `scenarios_p025_reference.txt` | 46 | Headline matrix on the reference land screen: six thermal trajectories × three oil paths, the EGS cases, the solar-premium break-evens |
| `scenarios_p025_lc.txt` | 18 | The same core configurations on the Class-C-only land screen |
| `scenarios_p025_jera120.txt` | 22 | Every JERA scenario re-solved at JERA's +20% capital case (the top of the reported band) |
| `scenarios_p025_advsolar.txt` | 86 | The full set on the ATB *Advanced* solar+battery basis (the cheaper-renewables supplement) |
| `scenarios_norps.txt` | 4 | The no-clean-energy-mandate cases (Section 4.6b) |
| `scenarios_lngconv.txt` / `scenarios_lngconv_heco.txt` | 3 + 1 | LNG-conversion cases: FSRU + existing-plant conversions with no new plant (Section 4.6a) |
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
variants and `R010_`/`R0015_` for gap refinements) belong to **v1.1**, the corrected
distributed-solar treatment (v1 as first circulated let rooftop PV retire to
zero by 2050; v1.1 fixes that). "v2" is reserved for the regional (nodal)
grid model described in `V2.md`. The prefixes are frozen because solve
fleets and refinement machinery reference them.

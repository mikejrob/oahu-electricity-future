# Base model

The starting-point Switch model of the Oʻahu grid: loads, existing fleet,
renewable resource characterizations, fuel-market structure, EV fleet, and
timescales. Developed by **Ethan Hartley** (with Matthias Fripp's
Switch-Hawaiʻi lineage); vendored here so this repository is fully
self-contained. `build/build_corrected_inputs.py` reads these directories,
applies the documented changes and additions (docs/CONVENTIONS.md), and
regenerates `inputs/` and `inputs_lu_constrained_c/` deterministically — the
committed inputs are byte-identical to that regeneration.

- `reference_wslope/inputs/` — reference land screen, graduated-slope solar
- `constrained_c/inputs/`   — Class-C-only land screen
- `modules.txt`             — the base module list (the build adapts it)

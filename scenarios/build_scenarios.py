#!/usr/bin/env python3
"""
build_scenarios.py
==================
Rewire the report's claimed scenarios onto the CORRECTED inputs, mechanically
and transparently. Reads the report working-tree scenario specs and emits
corrected specs with:

  * fabricated-solar alias REMOVED  (gen_build_costs.csv=gen_build_costs_atb25.csv
    -> use the corrected default gen_build_costs.csv, which is ATB 2024 x1.20)
  * EGS/pv variant aliases REMAPPED to the corrected variant files
    (gen_build_costs_egs_high_atb25.csv -> gen_build_costs_egs_high.csv, etc.)
  * nominal reference-Brent alias REMOVED (fuel_supply_curves_refbrent.csv
    -> use the corrected default = Ethan's REAL base). low/high brent aliases
    kept (they now point at the REAL variants built by build_brent_variants.py)
  * scenario / output names de-atb25'd ("atb25" was the fabrication label)
  * mipgap set for the requested two-pass solve (0.25% then 0.1%)
  * cold first pass: warm-start references to non-existent report outputs removed

Outputs: the scenarios_p025_*.txt first-pass lists (mipgap 0.0025, cold
start). The 0.1% refinement lists are generated separately by build_p001.py
once first-pass solutions exist.

Land-constrained (lc) scenarios reference inputs_lu_constrained_c. The
graduated-slope version of that dir (constrained_c_wslope) is a pending
methodology decision (see docs/OPEN_constrained_c_wslope.md); lc lines are
emitted but marked so the solve driver can hold them until the dir exists.
"""
import os
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent          # portable: this scenarios/ dir
# The report working tree the scenario specs are transformed FROM. Not part of
# this repo (separate, non-public). Needed ONLY to regenerate the scenario
# lists; the committed lists run without it. Override with RPT=/path.
RPT = Path(os.environ.get(
    "RPT", "/mnt/lustre/koa/koastore/gtg_group/Hawaii_EGS_Switch"))

SCENARIO_FILES = [
    "scenarios_atb25_baselines.txt", "scenarios_atb25_egs.txt",
    "scenarios_atb25_lc.txt", "scenarios_atb25_extension.txt",
    "scenarios_atb25_illustrative.txt", "scenarios_atb25_wb_lng500.txt",
    "scenarios_atb25_wr_lng.txt", "scenarios_breakeven.txt",
]

# input-file alias remaps (fabricated -> corrected)
ALIAS_REMAP = {
    "gen_build_costs_egs_high_atb25.csv": "gen_build_costs_egs_high.csv",
    "gen_build_costs_egs_low_atb25.csv": "gen_build_costs_egs_low.csv",
    "gen_build_costs_atb25_pv15.csv": "gen_build_costs_pv15.csv",
    "gen_build_costs_atb25_pv17.csv": "gen_build_costs_pv17.csv",
}


def transform(line, mipgap, cold):
    if not line.strip() or line.strip().startswith("#"):
        return None
    s = line.strip()

    # 1. drop the fabricated baseline-solar alias entirely (use corrected default)
    s = re.sub(r"--input-alias\s+gen_build_costs\.csv=gen_build_costs_atb25\.csv\s+",
               "", s)
    # 2. remap EGS/pv variant aliases to corrected files
    for old, new in ALIAS_REMAP.items():
        s = s.replace(old, new)
    # 3. drop the nominal reference-Brent alias (corrected default is real)
    s = re.sub(r"--input-alias\s+fuel_supply_curves\.csv=fuel_supply_curves_refbrent\.csv\s+",
               "", s)
    #    (low/high brent aliases remain; those files are now REAL variants)

    # 4. de-atb25 the scenario + output names
    s = s.replace("atb25lc_", "lc_").replace("outputs_atb25lc_", "outputs_lc_")
    s = s.replace("atb25_", "").replace("outputs_", "outputs_")

    # 5. mipgap for this pass
    s = re.sub(r"mipgap=[0-9.]+", f"mipgap={mipgap}", s)

    # 6. cold first pass: strip warm-start (report outputs don't exist here)
    if cold:
        s = re.sub(r"--warmstart-from\s+\S+\s*", "", s)
        s = re.sub(r"\bwarm_start_from_outputs\b", "", s)
        s = re.sub(r"mipstart=1", "mipstart=0", s)
    # tidy doubled spaces, then drop an --include-modules flag left empty by
    # the warm-start strip (switch errors on a bare flag)
    s = re.sub(r"\s{2,}", " ", s).strip()
    s = re.sub(r"--include-modules\s+(?=--)", "", s)
    return s


def build(mipgap, cold, outname):
    # The report's spec files list atb25_wb_C6_LNG500_{low,high}brent twice
    # (extension + wb_lng500 files), whitespace-identical. Dedupe by scenario
    # name so the set is the 64 UNIQUE runs the report actually solved.
    lines, seen = [], set()
    for fn in SCENARIO_FILES:
        p = RPT / fn
        if not p.exists():
            continue
        for raw in p.read_text().splitlines():
            t = transform(raw, mipgap, cold)
            if not t:
                continue
            name = re.search(r"--scenario-name (\S+)", t).group(1)
            if name in seen:
                continue
            seen.add(name)
            lines.append(t)
    (OUT / outname).write_text("\n".join(lines) + "\n")
    lc = sum(1 for x in lines if "inputs_lu_constrained_c" in x)
    print(f"{outname}: {len(lines)} unique scenarios ({len(lines)-lc} "
          f"reference-land, {lc} land-constrained)")
    # split into the two lists the solve driver actually submits:
    #   *_reference.txt  (46, inputs/)              solve/solve_p025_reference.slurm
    #   *_lc.txt         (18, inputs_lu_constrained_c/)  solve/solve_p025_lc.slurm
    ref = [x for x in lines if "inputs_lu_constrained_c" not in x]
    lc = [x for x in lines if "inputs_lu_constrained_c" in x]
    (OUT / outname.replace(".txt", "_reference.txt")).write_text("\n".join(ref) + "\n")
    (OUT / outname.replace(".txt", "_lc.txt")).write_text("\n".join(lc) + "\n")
    return len(lines)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    # Only the 0.25% (cold) pass is generated here. The 0.1% refinement pass is
    # NOT a simple re-run: each cell warm-starts from its own 0.25% solution, so
    # it is generated by scenarios/build_p001.py after the 0.25% cells solve.
    n = build("0.0025", cold=True, outname="scenarios_p025.txt")
    assert n == 64, f"expected 64 unique scenarios, got {n}"
    print("OK: 64 unique scenarios (46 reference-land + 18 land-constrained). "
          "0.1% pass: run scenarios/build_p001.py after the 0.25% solves.")

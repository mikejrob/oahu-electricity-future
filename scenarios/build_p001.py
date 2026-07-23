#!/usr/bin/env python3
"""
build_p001.py — generate the 0.1% refinement pass for scenarios already solved
at 0.25%, warm-started from their own p025 solutions.

For each cell whose outputs_<name>/total_cost.txt exists, emit a p001 line that:
  * warm-starts from outputs_<name>  (the p025 MIP solution, via
    warm_start_from_outputs -> CPLEX MIP start; mipstart=1)
  * writes to a SEPARATE dir outputs_p001_<name> (never clobber the source)
  * tightens mipgap 0.0025 -> 0.001
Cells whose p001 dir already has total_cost.txt are skipped (idempotent — safe
to re-run as more p025 cells finish). Prints the count so the launcher knows
whether there is anything new to submit.

Writes scenarios/scenarios_p001_ready.txt (ref + lc mixed; each line carries
its own --inputs-dir, so one array handles both).
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent    # portable: repo root from script
SRC = [REPO / "scenarios" / s for s in (
    "scenarios_p025_reference.txt", "scenarios_p025_lc.txt",
    "scenarios_p025_jera120.txt", "scenarios_p025_advsolar.txt",
    "scenarios_norps.txt", "scenarios_lngconv.txt",
    "scenarios_lngconv_heco.txt", "scenarios_pvjera.txt")]


def transform(line):
    name = re.search(r"--scenario-name (\S+)", line).group(1)
    p025 = REPO / f"outputs_{name}"
    if not (p025 / "total_cost.txt").exists():
        return None                      # p025 not solved yet
    if (REPO / f"outputs_p001_{name}" / "total_cost.txt").exists():
        return None                      # p001 already done
    s = line.strip()
    s = s.replace(f"--outputs-dir outputs_{name}",
                  f"--outputs-dir outputs_p001_{name}")
    s = re.sub(r"mipgap=0\.0025", "mipgap=0.001", s)
    s = re.sub(r"mipstart=0", "mipstart=1", s)
    # add warm-start: module + source dir
    if "--include-modules" in s:
        s = re.sub(r"(--include-modules (?:(?!--)\S+\s+)*)",
                   lambda m: m.group(1) + "warm_start_from_outputs ", s, count=1)
    else:
        s = s.replace(f"--outputs-dir outputs_p001_{name}",
                      f"--outputs-dir outputs_p001_{name} "
                      f"--include-modules warm_start_from_outputs")
    s = re.sub(r"(\s--solver-options-string)",
               f" --warmstart-from outputs_{name}\\1", s, count=1)
    return re.sub(r"\s{2,}", " ", s).strip()


def main():
    out = []
    for f in SRC:
        for line in f.read_text().splitlines():
            if line.strip():
                t = transform(line)
                if t:
                    out.append(t)
    dest = REPO / "scenarios" / "scenarios_p001_ready.txt"
    dest.write_text("\n".join(out) + ("\n" if out else ""))
    print(f"scenarios_p001_ready.txt: {len(out)} cells ready to refine")
    return len(out)


if __name__ == "__main__":
    main()

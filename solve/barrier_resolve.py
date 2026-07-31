#!/usr/bin/env python3
"""barrier_resolve.py — re-solve specific cells with 8-core barrier (mipalg=4).

The ITC cost-cliff makes the LP degenerate; dual simplex (the default) stalls
and can report a suboptimal incumbent as if converged. Barrier (mipalg=4) is
immune to the degeneracy but needs cores to parallelize its factorization.
Use this for cells flagged by sanity_check_results.py.

  python solve/barrier_resolve.py CELL [CELL ...]     # explicit names
  python solve/barrier_resolve.py --from-sanity        # read /tmp/sanity_flagged.txt

Writes scenarios/scenarios_barrier.txt and prints an sbatch-ready count.
EGS cost-sensitivity cells (egs_low_*/egs_high_*) are additionally pinned to
EGS=100 (gen_info_egs100) — EGS is bang-bang, so the marginal decision is
removed and only the barrier fix for degeneracy remains.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LISTS = [REPO / "scenarios" / f for f in (
    "scenarios_p025_reference.txt", "scenarios_p025_lc.txt",
    "scenarios_p025_jera120.txt", "scenarios_p025_advsolar.txt",
    "scenarios_norps.txt", "scenarios_lngconv.txt",
    "scenarios_lngconv_heco.txt", "scenarios_pvjera.txt")]

if "--from-sanity" in sys.argv:
    cells = Path("/tmp/sanity_flagged.txt").read_text().split()
else:
    cells = [a for a in sys.argv[1:] if not a.startswith("-")]

orig = {}
for f in LISTS:
    if f.exists():
        for line in f.read_text().splitlines():
            m = re.search(r"--scenario-name (\S+)", line)
            if m:
                orig[m.group(1)] = line.strip()

out = []
for name in cells:
    if name not in orig:
        print(f"  no scenario line for {name}", file=sys.stderr)
        continue
    s = orig[name]
    # EGS sensitivity cells: pin EGS=100 (bang-bang corner)
    if re.match(r"egs_(low|high)_", name):
        s = s.replace("--inputs-dir inputs",
                      "--inputs-dir inputs --input-alias gen_info.csv=gen_info_egs100.csv", 1)
    # barrier root + drop conservative emphases + 8 threads
    s = re.sub(r"numericalemphasis=1", "mipalg=4 numericalemphasis=0", s)
    s = re.sub(r"memoryemphasis=1", "memoryemphasis=0", s)
    s = re.sub(r"threads=1", "threads=8", s)
    out.append(re.sub(r"\s{2,}", " ", s).strip())
    # clear the stale (stuck) output so it re-solves fresh
    d = REPO / f"outputs_{name}"
    if d.exists():
        import shutil
        shutil.rmtree(d)

dest = REPO / "scenarios" / "scenarios_barrier.txt"
dest.write_text("\n".join(out) + ("\n" if out else ""))
print(f"scenarios_barrier.txt: {len(out)} cells for 8-core barrier re-solve")
for l in out:
    print("  ", re.search(r"--scenario-name (\S+)", l).group(1))

#!/usr/bin/env python3
"""build_p001_retry.py — second 0.1% attempt for the hard (0.15%) cells.

After the hard cells solve at 0.15% (scenarios_p001_015.txt -> outputs_p001_*),
retry each at the full 0.1% gap, warm-started from its OWN 0.15% solution — a
much tighter incumbent than the 0.25% start, so a better chance of closing the
last sliver. Any cell that reaches 0.1% is a small update; any that does not is
kept at 0.15%. Idempotent: only emits cells whose 0.15% solve exists and whose
0.1% retry has not yet been confirmed at <=0.1% (tracked by a .p001_gap marker).

Writes scenarios/scenarios_p001_retry.txt. The retry writes to a temp dir and
only overwrites outputs_p001_<name> if it genuinely reaches 0.1%.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HARD = [c.strip("- `") for c in
        (REPO / "docs" / "HARD_CELLS.md").read_text().splitlines()
        if c.startswith("- `")]
SRC = [REPO / "scenarios" / s for s in (
    "scenarios_p025_reference.txt", "scenarios_p025_lc.txt",
    "scenarios_p025_jera120.txt", "scenarios_p025_advsolar.txt",
    "scenarios_norps.txt", "scenarios_lngconv.txt",
    "scenarios_lngconv_heco.txt", "scenarios_pvjera.txt")]
lines = {}
for f in SRC:
    if f.exists():
        for l in f.read_text().splitlines():
            m = re.search(r"--scenario-name (\S+)", l)
            if m:
                lines[m.group(1)] = l.strip()

out = []
for name in HARD:
    if name not in lines:
        continue
    # need a 0.15% solution to warm-start from
    if not (REPO / f"outputs_p001_{name}" / "total_cost.txt").exists():
        continue
    # skip if already confirmed at 0.1% (marker written by the retry wrapper)
    if (REPO / f"outputs_p001_{name}" / ".confirmed_p001").exists():
        continue
    s = lines[name]
    s = s.replace(f"--outputs-dir outputs_{name}",
                  f"--outputs-dir outputs_p001retry_{name}")
    s = re.sub(r"mipgap=0\.0025", "mipgap=0.001", s)
    s = re.sub(r"mipstart=0", "mipstart=1", s)
    # warm-start from the 0.15% solution (its own outputs_p001_ dir)
    if "--include-modules" in s:
        s = re.sub(r"(--include-modules (?:(?!--)\S+\s+)*)",
                   lambda m: m.group(1) + "warm_start_from_outputs ", s, count=1)
    else:
        s = s.replace(f"--outputs-dir outputs_p001retry_{name}",
                      f"--outputs-dir outputs_p001retry_{name} "
                      f"--include-modules warm_start_from_outputs")
    s = re.sub(r"(\s--solver-options-string)",
               f" --warmstart-from outputs_p001_{name}\\1", s, count=1)
    out.append(re.sub(r"\s{2,}", " ", s).strip())

dest = REPO / "scenarios" / "scenarios_p001_retry.txt"
dest.write_text("\n".join(out) + ("\n" if out else ""))
print(f"scenarios_p001_retry.txt: {len(out)} hard cells ready for the 0.1% retry")
